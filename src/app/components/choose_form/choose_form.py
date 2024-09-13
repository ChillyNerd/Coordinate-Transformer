import dash_bootstrap_components as dbc
from dash import html, Output, Input, State
from dash.exceptions import PreventUpdate

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.coordinate_transformer import projections_dict
from src.coordinate_transformer.enums import ProjectionGroup, Metrics


class ChooseForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
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
        projections_group_form = html.Div(children=[projections_group_label, projections_group_input],
                                          className="row-between")

        zone_from_label = html.Div("Исходная зона", className='label-form common-label')
        zone_from_input = dbc.Select(id='zone_from_select', className="common-input")
        zone_from_form = html.Div(children=[zone_from_label, zone_from_input], className="row-between")

        self.layout = html.Div(children=[choose_form_label, metrics_form, projections_group_form, zone_from_form],
                               className="column-gap")
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback(
            [
                Output('zone_from_select', 'options'),
                Output('zone_from_select', 'value'),
                Output('input_angle_form', 'className'),
                Output('input_numeric_form', 'className')
            ], [
                Input('metrics_select', 'value'),
                Input('projection_from_select', 'value'),
                State('input_angle_form', 'className'),
                State('input_numeric_form', 'className'),
            ]
        )
        def select_input_form(metric_name, projection_from, angle_class_name, numeric_class_name):
            if metric_name is None:
                raise PreventUpdate
            angle_classes = angle_class_name.split()
            numeric_classes = numeric_class_name.split()
            projections = projections_dict.values()
            zones_from = list(filter(
                lambda projection: metric_name in [metric.name for metric in Metrics if
                                                   metric.value.metric_type == projection.metric_type] and not projection.disabled and projection.projection_group == projection_from,
                projections
            ))
            projections_from_options = [{'label': proj.comment, 'value': proj.mnemonic} for proj in zones_from]
            if metric_name == Metrics.METER.name or metric_name == Metrics.FLOAT_ANGLE.name:
                if self.hidden not in angle_classes:
                    angle_classes.append(self.hidden)
                if self.hidden in numeric_classes:
                    numeric_classes = list(filter(lambda class_name: class_name != self.hidden, numeric_classes))
            if metric_name == Metrics.ANGLE.name:
                if self.hidden in angle_classes:
                    angle_classes = list(filter(lambda class_name: class_name != self.hidden, angle_classes))
                if self.hidden not in numeric_classes:
                    numeric_classes.append(self.hidden)
            return projections_from_options, None, ' '.join(angle_classes), ' '.join(numeric_classes)

        @self.dash_app.callback(
            [
                Output('input_tabs', 'className')
            ], [
                Input('metrics_select', 'value'),
                Input('zone_from_select', 'value'),
                State('input_tabs', 'className')
            ]
        )
        def show_input_form(selected_metric, selected_projection, tabs_classes):
            classes = tabs_classes.split()
            if selected_metric is None or selected_projection is None:
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]
