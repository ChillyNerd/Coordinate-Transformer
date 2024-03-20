import os
import pandas as pd
from src.excel_transformer.transform_exception import FileIsNotExcel, FileIsEmpty, FileHasNoColumns
from src.coordinate_transformer.coordinate_transformer import CoordinateTransformer
from src.coordinate_transformer.impl import Projection


class ExcelTransformer:
    def __init__(self, projection_from: Projection, projection_to: Projection, latitude_column: int, longitude_column: int):
        self.coordinate_transformer = CoordinateTransformer(projection_from, projection_to)
        self.latitude_column = latitude_column
        self.longitude_column = longitude_column

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
        latitude, longitude = self.coordinate_transformer.transform(
            row.iloc[self.latitude_column], row.iloc[self.longitude_column]
        )
        return pd.Series({'latitude': latitude, 'longitude': longitude})
