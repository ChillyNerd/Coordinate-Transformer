import dash_bootstrap_components as dbc
from dash import html

from src.coordinate_transformer import projections_dict

projections_to_label = html.Div("Ключевая проекция", style={"width": "40%"}, className='label-form')
projections_to_input = dbc.Select(
    options=[{'label': proj.comment, 'value': proj.mnemonic} for proj in projections_dict.values()],
    id='projection_to_select', style={"width": "60%"}
)
projections_to_form = html.Div(children=[projections_to_label, projections_to_input], id='projection-to-form',
                               className="row-between padding-top border-top")
