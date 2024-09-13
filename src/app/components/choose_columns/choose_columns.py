import traceback

import dash_bootstrap_components as dbc
from dash import html, Output, Input, State
from dash.exceptions import PreventUpdate

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.excel_transformer import ExcelTransformer, BaseExcelTransformException


class ChooseColumns(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        latitude_column_label = html.Div("Колонка широты", className='label-form')
        latitude_column_input = dbc.Select(id='latitude_column_select')
        latitude_column_form = html.Div(children=[latitude_column_label, latitude_column_input],
                                        className="row-between")

        longitude_column_label = html.Div("Колонка долготы", className='label-form')
        longitude_column_input = dbc.Select(id='longitude_column_select')
        longitude_column_form = html.Div(children=[longitude_column_label, longitude_column_input],
                                         className="row-between")

        choose_column_dialog_body = html.Div([latitude_column_form, longitude_column_form], className='column-gap')

        choose_column_dialog = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Выбор колонок")),
                dbc.ModalBody(choose_column_dialog_body),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Подтвердить выбор", id="confirm_columns", n_clicks=0
                        )
                    ]
                )
            ],
            id="choose_column_dialog",
            backdrop='static',
            centered=True,
            is_open=False,
        )
        self.layout = choose_column_dialog
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback(
            Output('excel_columns', 'data'),
            Output('excel_read_error', 'data'),
            Input('excel_file', 'data'),
        )
        def read_excel(excel_file):
            if excel_file is None:
                return None, None
            try:
                return ExcelTransformer.get_excel_columns(excel_file), None
            except BaseExcelTransformException as ex:
                self.app.log.exception(ex)
                return None, ex.message
            except Exception as ex:
                self.app.log.exception(ex)
                return None, traceback.format_exc()

        @self.dash_app.callback(
            Output('longitude_column_select', 'options'),
            Output('latitude_column_select', 'options'),
            Input('excel_columns', 'data'),
        )
        def set_column_options(columns):
            if columns is None:
                return None, None
            options = [{'label': column, 'value': index} for index, column in enumerate(columns)]
            return options, options

        @self.dash_app.callback(
            Output('latitude_column_select', 'value'),
            Input('latitude_column_select', 'options'),
        )
        def null_latitude_column_value(latitude_select):
            return None

        @self.dash_app.callback(
            Output('longitude_column_select', 'value'),
            Input('longitude_column_select', 'options'),
        )
        def null_longitude_column_value(longitude_select):
            return None

        @self.dash_app.callback(
            Output('choose_column_dialog', 'is_open'),
            Input('toggle_choose_column_dialog', 'data'),
            Input('inspect_excel_file', 'n_clicks'),
            Input('confirm_columns', 'n_clicks'),
            State('choose_column_dialog', 'is_open')
        )
        def toggle_choose_column_dialog(toggle, inspect_clicks, delete_clicks, is_open):
            if toggle is None or not toggle:
                raise PreventUpdate
            is_open = not is_open
            return is_open

        @self.dash_app.callback(
            Output('toggle_choose_column_dialog', 'data'),
            Input('excel_columns', 'data')
        )
        def choose_columns(columns):
            if columns is None:
                return False
            return True
