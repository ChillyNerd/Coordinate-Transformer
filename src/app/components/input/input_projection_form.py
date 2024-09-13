import dash_bootstrap_components as dbc
from dash import html, Output, Input, State

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.coordinate_transformer import projections_dict
from src.coordinate_transformer.enums import ProjectionGroup


class ProjectionToForm(BaseComponent):
    def __init__(self, app: AbstractApp):
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
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback(
            Output('zone_to_select', 'options'),
            Output('zone_to_select', 'value'),
            Input('projection_to_select', 'value')
        )
        def filter_zones(group_name):
            projections = list(filter(
                lambda projection: projection.projection_group == group_name, projections_dict.values()
            ))
            return [{'label': projection.comment, 'value': projection.mnemonic} for projection in projections], None

        @self.dash_app.callback(
            [
                Output('projection_to_form', 'className')
            ], [
                Input('points', 'data'),
                Input('shape_files', 'data'),
                State('tabs_select', 'active_tab'),
                State('projection_to_form', 'className')
            ]
        )
        def show_projection_to_form(points, shape_files, selected_tab, projection_classes):
            classes = projection_classes.split()
            if selected_tab == 'shape_tab':
                should_be_hidden = shape_files is None
            else:
                should_be_hidden = points is None or len(points) == 0
            if should_be_hidden:
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]

        @self.dash_app.callback([
            Output('zone_to_form', 'className')
        ], [
            Input('points', 'data'),
            Input('shape_files', 'data'),
            Input('projection_to_select', 'value'),
            State('tabs_select', 'active_tab'),
            State('zone_to_form', 'className')
        ])
        def show_zone_select_form(points, shape_files, projection_group, selected_tab, output_classes):
            classes = output_classes.split()
            should_be_hidden = projection_group is None
            if selected_tab == 'shape_tab':
                should_be_hidden = should_be_hidden or shape_files is None
            else:
                should_be_hidden = should_be_hidden or points is None or len(points) == 0
            if should_be_hidden:
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]
