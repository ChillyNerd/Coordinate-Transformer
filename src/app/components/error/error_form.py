import dash_bootstrap_components as dbc
from dash import Dash, Output, Input

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent


class ErrorForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        form = dbc.Alert(dismissable=True, color='warning', is_open=False, id='error', duration=4000,
                         className="error-form")
        self.layout = form
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback([
            Output('error', 'children'),
            Output('error', 'is_open')
        ], [
            Input('transform_error', 'data'),
            Input('excel_upload_error', 'data'),
            Input('excel_show_error', 'data'),
            Input('excel_read_error', 'data'),
            Input('shape_read_error', 'data')
        ])
        def set_error(transform_error, excel_upload_error, excel_show_error, excel_read_error, shape_read_error):
            errors = []
            if transform_error is not None:
                errors.append(transform_error)
            if excel_upload_error is not None:
                errors.append(excel_upload_error)
            if excel_read_error is not None:
                errors.append(excel_read_error)
            if excel_show_error is not None:
                errors.append(excel_show_error)
            if shape_read_error is not None:
                errors.append(shape_read_error)
            if len(errors) == 0:
                return None, False
            return '\n'.join(errors), True
