import dash_bootstrap_components as dbc
from dash import html

from src.coordinate_transformer.enums import ProjectionGroup, Metrics

choose_form_label = html.Div("Параметры пересчета")
metrics_label = html.Div("Единицы измерения", className='label-form common-label')
metrics_select = dbc.Select(
    options=[{'label': metric.value.label, 'value': metric.name} for metric in Metrics],
    id='metrics_select',
    value=Metrics.METER.name,
    className="common-input"
)
metrics_form = html.Div(children=[metrics_label, metrics_select], className="row-between")

projections_group_label = html.Div("Исходная проекция", className='label-form common-label')
projections_group_input = dbc.Select(
    options=[{'label': group.value, 'value': group.name} for group in ProjectionGroup],
    id='projection_from_select', className='common-input', value=ProjectionGroup.GSK_SK.name
)
projections_group_form = html.Div(children=[projections_group_label, projections_group_input], className="row-between")

zone_from_label = html.Div("Исходная зона", className='label-form common-label')
zone_from_input = dbc.Select(id='zone_from_select', className="common-input")
zone_from_form = html.Div(children=[zone_from_label, zone_from_input], className="row-between")

form = html.Div(children=[choose_form_label, metrics_form, projections_group_form, zone_from_form], className="column-gap")
