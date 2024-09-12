from dash import html, Dash, Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.coordinate_transformer import projections_dict
from src.coordinate_transformer.enums import OutputMetrics


class OutputManualForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        result_metrics_select = dbc.Select(
            id='output_metrics_select',
            className="common-input"
        )
        result_label = html.Div("Результат", className="label-form common-label")
        output_form_label = html.Div([result_label, result_metrics_select], className='row-between')

        result_latitude_label = html.Div("Широта", className='label-form common-label')
        result_latitude_value = html.Div(id='result_latitude')
        result_latitude_form = html.Div(children=[result_latitude_label, result_latitude_value],
                                        className='row-between')
        result_longitude_label = html.Div("Долгота", className='label-form common-label')
        result_longitude_value = html.Div(id='result_longitude')
        result_longitude_form = html.Div(children=[result_longitude_label, result_longitude_value],
                                         className='row-between')
        form = html.Div(
            children=[output_form_label, result_latitude_form, result_longitude_form],
            className="column-gap border-top padding-top", id='output_manual_form'
        )
        self.layout = form
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback([
                Output('output_manual_form', 'className')
            ], [
                Input('result_latitude', 'children'),
                Input('result_longitude', 'children'),
                Input('tabs_select', 'active_tab'),
                State('output_manual_form', 'className')
            ]
        )
        def show_manual_result(result_latitude, result_longitude, active_tab, class_names):
            classes = class_names.split()
            if result_latitude is None or result_longitude is None or active_tab != 'manual_tab':
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]

        @self.dash_app.callback(
            Output('output_metrics_select', 'options'),
            Output('output_metrics_select', 'value'),
            Input('zone_to_select', 'value'),
        )
        def set_output_metrics(zone_name):
            if zone_name is None:
                raise PreventUpdate
            zone_to = projections_dict[zone_name]
            allowed_metrics = [{'label': metric.value.label, 'value': metric.name} for metric in OutputMetrics if
                               metric.value.metric_type == zone_to.metric_type]
            return allowed_metrics, allowed_metrics[0]['value']
