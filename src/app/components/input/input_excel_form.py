import traceback

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
from flask import request

from src.app.abstract_app import AbstractApp
from src.app.assets.icons import delete_icon, inspect_icon
from src.app.components import BaseComponent
from src.coordinate_transformer import projections_dict
from src.excel_transformer import ExcelTransformer, BaseExcelTransformException


class InputExcelForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        upload_button = dcc.Upload(dbc.Button('Загрузить файл'), id='upload_excel_file', className="upload-file")
        delete_button = dbc.Button(
            html.Img(src=delete_icon, className='common-icon'),
            id='delete_excel_file', color='danger', className='action-button align-center'
        )
        inspect_button = dbc.Button(
            html.Img(src=inspect_icon, className='common-icon'),
            id='inspect_excel_file', color='secondary', className='action-button align-center'
        )
        buttons = html.Div(children=[upload_button, delete_button, inspect_button], className='row-gap')
        excel_file_name = html.Div('Выберите файл', id='excel_file_name', className="file-name")
        form = html.Div(children=[buttons, excel_file_name], className="upload-form row-gap long-gap")
        self.layout = form
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback([
            Output('excel_file', 'data'),
            Output('excel_file_name', 'children'),
            Output('excel_upload_error', 'data')
        ], [
            Input('upload_excel_file', 'contents'),
            State('upload_excel_file', 'filename')
        ])
        def upload_excel_file(file_content, file_name):
            if not file_name:
                return None, 'Выберите файл', None
            try:
                file = {'filename': file_name, 'content': file_content}
                path = self.app.upload_file(request.remote_addr, 'excel_input', file)
                self.app.log.info(f'{request.remote_addr} successfully uploaded excel file {file_name}')
                return path, file_name, None
            except Exception as ex:
                self.app.log.exception(ex)
                return None, 'Выберите файл', traceback.format_exc()

        @self.dash_app.callback(
            [
                Output('upload_excel_file', 'contents'),
                Output('upload_excel_file', 'filename')
            ], [
                Input('delete_excel_file', 'n_clicks')
            ])
        def clear_excel_file(clicks):
            if clicks:
                self.app.delete_files(request.remote_addr, 'excel_input')
                return None, None
            else:
                raise PreventUpdate

        @self.dash_app.callback([
            Output('excel_points', 'data'),
            Output('excel_show_error', 'data')
        ], [
            Input('confirm_columns', 'n_clicks'),
            Input('zone_from_select', 'value'),
            Input('latitude_column_select', 'value'),
            Input('longitude_column_select', 'value'),
            State('excel_file', 'data'),
            State('metrics_select', 'value')
        ])
        def set_excel_points(confirm_clicks, projection_from, latitude_column, longitude_column, excel_file, metric):
            if excel_file is None or projection_from is None or latitude_column is None or longitude_column is None:
                return None, None
            try:
                transformer = ExcelTransformer(
                    projection_from=projections_dict[projection_from],
                    projection_to=projections_dict["epsg:4326"],
                    latitude_column=int(latitude_column),
                    longitude_column=int(longitude_column),
                    metric=metric
                )
                points = []
                df = transformer.transform(excel_file)
                for index in range(len(df)):
                    row = df.iloc[index]
                    points.append(
                        {'latitude': row['result_latitude'], 'longitude': row['result_longitude'], 'id': index})
                return points, None
            except BaseExcelTransformException as ex:
                self.app.log.exception(ex)
                return None, ex.message
            except Exception as ex:
                self.app.log.exception(ex)
                return None, traceback.format_exc()
