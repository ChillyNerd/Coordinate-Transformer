from src.coordinate_transformer.defaults import Metrics
import dash_bootstrap_components as dbc
from dash import html

from src.coordinate_transformer import projections_dict

choose_form_label = html.Div("Параметры пересчета")
metrics_label = html.Div("Метрика", className='label-form')
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
projections_to_label = html.Div("Ключевая проекция", style={"width": "40%"}, className='label-form')
projections_to_input = dbc.Select(
    options=[{'label': proj.comment, 'value': proj.mnemonic} for proj in projections_dict.values()],
    id='projection_to_select', style={"width": "60%"}
)
projections_to_form = html.Div(children=[projections_to_label, projections_to_input], className="row-between")
form = html.Div(children=[choose_form_label, metrics_form, projections_from_form, projections_to_form],
                className="column-gap choose-form")
