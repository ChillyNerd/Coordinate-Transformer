from dash import dcc, html
from src.coordinate_transformer.defaults import Metrics
import dash_bootstrap_components as dbc

input_form_label = html.Div("Входные координаты")
metrics_label = html.Div("Метрика")
metrics_select = dbc.Select(
    options=[{'label': metric.value, 'value': metric.name} for metric in Metrics],
    id='metrics_select',
    value=Metrics.METER.name
)
metrics_form = html.Div(children=[metrics_label, metrics_select], className="row-between")
input_form = html.Div(id='input_form')
form = html.Div(children=[input_form_label, metrics_form, input_form], className="column-gap input-form")
