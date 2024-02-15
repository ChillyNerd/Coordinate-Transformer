import dash_bootstrap_components as dbc
from dash import html

from src.coordinate_transformer.defaults import Metrics

choose_form_label = html.Div("Параметры пересчета")
metrics_label = html.Div("Единицы измерения", className='label-form')
metrics_select = dbc.Select(
    options=[{'label': metric.value, 'value': metric.name} for metric in Metrics],
    id='metrics_select',
    value=Metrics.METER.name,
    className="metric-select"
)
metrics_form = html.Div(children=[metrics_label, metrics_select], className="row-between")
projections_from_label = html.Div("Исходная проекция", style={"width": "40%"}, className='label-form')
projections_from_input = dbc.Select(id='projection_from_select', style={"width": "60%"})
projections_from_form = html.Div(children=[projections_from_label, projections_from_input], className="row-between")
form = html.Div(children=[choose_form_label, metrics_form, projections_from_form], className="column-gap")
