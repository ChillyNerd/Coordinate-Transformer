from dash import html, Dash
import dash_bootstrap_components as dbc

from src.app.components import BaseComponent


class OutputManualForm(BaseComponent):
    def __init__(self, app: Dash):
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

    def init_callbacks(self):
        pass
