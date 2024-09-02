import dash_bootstrap_components as dbc
from dash import html

from src.coordinate_transformer import projections_dict
from src.coordinate_transformer.enums import ProjectionGroup

projections_group_label = html.Div("Ключевая проекция", style={"width": "40%"}, className='label-form')
projections_group_input = dbc.Select(
    options=[{'label': group.value, 'value': group.name} for group in ProjectionGroup],
    id='projection_to_select', style={"width": "60%"}
)
projections_group_form = html.Div(children=[projections_group_label, projections_group_input], 
                                  id='projection_to_form', className="row-between padding-top border-top")

zone_to_label = html.Div("Ключевая зона", style={"width": "40%"}, className='label-form')
zone_to_input = dbc.Select(
    id='zone_to_select', style={"width": "60%"}
)
zone_to_form = html.Div(children=[zone_to_label, zone_to_input], id='zone_to_form',
                               className="row-between padding-top")

projection_to_form = html.Div(children=[projections_group_form, zone_to_form])
