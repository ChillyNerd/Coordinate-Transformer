import dash_bootstrap_components as dbc
from dash import html, Dash

from src.app.components import BaseComponent
from src.coordinate_transformer.enums import ProjectionGroup


class ProjectionToForm(BaseComponent):
    def __init__(self, app: Dash):
        super().__init__(app)
        projections_group_label = html.Div("Ключевая проекция", className='label-form common-label')
        projections_group_input = dbc.Select(
            options=[{'label': group.value, 'value': group.name} for group in ProjectionGroup],
            id='projection_to_select', className='common-input'
        )
        projections_group_form = html.Div(children=[projections_group_label, projections_group_input],
                                          id='projection_to_form', className="row-between padding-top border-top")

        zone_to_label = html.Div("Ключевая зона", className='label-form common-label')
        zone_to_input = dbc.Select(
            id='zone_to_select', className='common-input'
        )
        zone_to_form = html.Div(children=[zone_to_label, zone_to_input], id='zone_to_form',
                                className="row-between padding-top")

        projection_to_form = html.Div(children=[projections_group_form, zone_to_form])
        self.layout = projection_to_form

    def init_callbacks(self):
        pass
