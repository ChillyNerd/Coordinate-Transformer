import os

import pandas as pd

from src.coordinate_transformer.coordinate_formater import string_angle_to_float
from src.coordinate_transformer.coordinate_transformer import CoordinateTransformer
from src.coordinate_transformer.enums import Metrics
from src.coordinate_transformer.impl import Projection
from src.excel_transformer.transform_exception import (FileIsNotExcel, FileIsEmpty, FileHasNoColumns,
                                                       NonCompatibleLatitude, NonCompatibleLongitude)


class ExcelTransformer:
    def __init__(self, projection_from: Projection, projection_to: Projection,
                 latitude_column: int, longitude_column: int, metric: str):
        self.coordinate_transformer = CoordinateTransformer(projection_from, projection_to)
        self.latitude_column = latitude_column
        self.longitude_column = longitude_column
        self.metric: str = metric

    @staticmethod
    def get_excel_columns(filepath: str):
        file_ext = os.path.splitext(filepath)[1]
        if file_ext.lower() not in ['.xlsx', '.xls']:
            raise FileIsNotExcel()
        excel_table = pd.read_excel(filepath, header=None)
        if excel_table.shape[0] == 0:
            raise FileIsEmpty()
        if excel_table.shape[1] < 2:
            raise FileHasNoColumns()
        return excel_table.iloc[0].tolist()

    def transform(self, file_path: str):
        excel_table = pd.read_excel(file_path, header=0)
        excel_table[['result_latitude', 'result_longitude']] = excel_table.apply(self.transform_one_row, axis=1)
        return excel_table

    def transform_one_row(self, row):
        latitude, longitude = row.iloc[self.latitude_column], row.iloc[self.longitude_column]
        if self.metric == Metrics.ANGLE.name:
            if not isinstance(latitude, str):
                raise NonCompatibleLatitude()
            latitude_values = latitude.split()
            if 2 > len(latitude_values) > 3:
                raise NonCompatibleLatitude()
            if not isinstance(longitude, str):
                raise NonCompatibleLongitude()
            longitude_values = longitude.split()
            if 2 > len(longitude_values) > 3:
                raise NonCompatibleLongitude()
            latitude = string_angle_to_float(*latitude_values)
            longitude = string_angle_to_float(*longitude_values)
        if not isinstance(latitude, (int, float)):
            raise NonCompatibleLatitude()
        if not isinstance(longitude, (int, float)):
            raise NonCompatibleLongitude()
        result_latitude, result_longitude = self.coordinate_transformer.transform(latitude, longitude)
        return pd.Series({'latitude': result_latitude, 'longitude': result_longitude})
