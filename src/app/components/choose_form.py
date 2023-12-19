import dash_bootstrap_components as dbc
from dash import html

from src.coordinate_transformer import projections_to, projections_from

choose_form_label = html.Div("Choose")
projections_from_label = html.Div("Choose projection from")
projections_from_input = dbc.Select(
    options=[{'label': proj.comment, 'value': proj.mnemonic} for proj in projections_from],
    id='projection_from_select'
)
projections_from_value = html.Div(id='projection_from_value')
projections_from_form = html.Div(children=[projections_from_label, projections_from_input, projections_from_value],
                                 className="row-between")
projections_to_label = html.Div("Choose projection to")
projections_to_input = dbc.Select(
    options=[{'label': proj.comment, 'value': proj.mnemonic} for proj in projections_to],
    id='projection_to_select'
)
projections_to_value = html.Div(id='projection_to_value')
projections_to_form = html.Div(children=[projections_to_label, projections_to_input, projections_to_value],
                               className="row-between")
form = html.Div(children=[choose_form_label, projections_from_form, projections_to_form],
                className="column-gap choose-form")
