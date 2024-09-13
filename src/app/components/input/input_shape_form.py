import traceback

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
from flask import request

from src.app.abstract_app import AbstractApp
from src.app.assets.icons import delete_icon
from src.app.components import BaseComponent
from src.shape_reader import ShapeReader, BaseShapeReadException


class InputShapeForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        upload_button = dcc.Upload(dbc.Button('Загрузить файл'), id='upload_shape_file', className="upload-file")
        delete_button = dbc.Button(
            html.Img(src=delete_icon, className='common-icon'),
            id='delete_shape_file', color='danger', className='action-button align-center'
        )
        buttons = html.Div(children=[upload_button, delete_button], className='row-gap')
        excel_file_name = html.Div('Выберите файл', id='shape_file_name', className="file-name")
        form = html.Div(children=[buttons, excel_file_name], className="upload-form row-gap long-gap")
        self.layout = form
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback([
            Output('shape_archive', 'data'),
            Output('shape_file_name', 'children'),
            Output('shape_upload_error', 'data')
        ], [
            Input('upload_shape_file', 'contents'),
            State('upload_shape_file', 'filename')
        ])
        def upload_shape_file(file_content, file_name):
            if not file_name:
                return None, 'Выберите файл', None
            try:
                file = {'filename': file_name, 'content': file_content}
                path = self.app.upload_file(request.remote_addr, 'shape_input', file)
                self.app.log.info(f'{request.remote_addr} successfully uploaded shape file {file_name}')
                return path, file_name, None
            except Exception as ex:
                self.app.log.exception(ex)
                return None, 'Выберите файл', traceback.format_exc()

        @self.dash_app.callback([
            Output('upload_shape_file', 'contents'),
            Output('upload_shape_file', 'filename')
        ], [
            Input('delete_shape_file', 'n_clicks')
        ])
        def clear_shape_file(clicks):
            if clicks:
                self.app.delete_files(request.remote_addr, 'shape_input')
                return None, None
            else:
                raise PreventUpdate

        @self.dash_app.callback(
            Output('shape_files', 'data'),
            Output('shape_read_error', 'data'),
            Input('shape_archive', 'data')
        )
        def read_shape(shape_archive):
            if shape_archive is None:
                return None, None
            try:
                return ShapeReader.read(shape_archive), None
            except BaseShapeReadException as ex:
                self.app.log.exception(ex)
                return None, ex.message
            except Exception as ex:
                self.app.log.exception(ex)
                return None, traceback.format_exc()
