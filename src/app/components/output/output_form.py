from dash import html, Dash, Output, Input, State

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.app.components.output.output_excel_form import OutputExcelForm
from src.app.components.output.output_manual_form import OutputManualForm
from src.app.components.output.output_shape_form import OutputShapeForm


class OutputForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        form = html.Div(
            children=[
                OutputShapeForm(self.app).get_layout(),
                OutputExcelForm(self.app).get_layout(),
                OutputManualForm(self.app).get_layout()
            ],
            className="column-gap",
            id='output_form'
        )
        self.layout = form
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback([
            Output('output_form', 'className')
        ], [
            Input('zone_from_select', 'value'),
            Input('zone_to_select', 'value'),
            State('output_form', 'className')
        ])
        def show_output_form(projection_from, projection_to, output_classes):
            classes = output_classes.split()
            if projection_from is None or projection_to is None:
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]
