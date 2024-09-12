from dash import dcc, html, Dash, Output, Input

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.coordinate_transformer import Metrics


class InputNumericForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        latitude_label = html.Div("Широта", className='common-label')
        latitude_input = dcc.Input(id='latitude_numeric_input', type='number', className="common-input")
        latitude_form = html.Div(children=[latitude_label, latitude_input], className='row-between')
        longitude_label = html.Div("Долгота", className='common-label')
        longitude_input = dcc.Input(id='longitude_numeric_input', type='number', className="common-input")
        longitude_form = html.Div(children=[longitude_label, longitude_input], className='row-between')

        form = html.Div(children=[latitude_form, longitude_form], className='column-gap', id='input_numeric_form')
        self.layout = form
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback(
            Output('numeric_longitude', 'data'),
            Input('longitude_numeric_input', 'value'),
            Input('metrics_select', 'value')
        )
        def set_numeric_longitude(longitude, metric):
            if metric == Metrics.ANGLE.name:
                return None
            return longitude

        @self.dash_app.callback(
            Output('numeric_latitude', 'data'),
            Input('latitude_numeric_input', 'value'),
            Input('metrics_select', 'value')
        )
        def set_numeric_latitude(latitude, metric):
            if metric == Metrics.ANGLE.name:
                return None
            return latitude

        @self.dash_app.callback(
            [
                Output('latitude_numeric_input', 'min'),
                Output('latitude_numeric_input', 'max'),
                Output('longitude_numeric_input', 'min'),
                Output('longitude_numeric_input', 'max')
            ], [
                Input('metrics_select', 'value')
            ]
        )
        def set_input_limit(metric):
            if metric == Metrics.FLOAT_ANGLE.name:
                return -90, 90, -180, 180
            return None, None, None, None
