from dash import html
import dash_bootstrap_components as dbc
from src.coordinate_transformer.defaults import Metrics

output_form_label = html.Div("Результат")
result_metrics_select = dbc.Select(
    options=[{'label': metric.value, 'value': metric.name} for metric in Metrics],
    id='metrics_select',
    value=Metrics.METER.name,
    className="common-input"
)
result_latitude_label = html.Div("Широта", className='label-form')
result_latitude_value = html.Div(id='result_latitude')
result_latitude_form = html.Div(children=[result_latitude_label, result_latitude_value], className='row-between')
result_longitude_label = html.Div("Долгота", className='label-form')
result_longitude_value = html.Div(id='result_longitude')
result_longitude_form = html.Div(children=[result_longitude_label, result_longitude_value], className='row-between')
form = html.Div(children=[output_form_label, result_latitude_form, result_longitude_form],
                className="column-gap border-top padding-top", id='output-manual-form')
