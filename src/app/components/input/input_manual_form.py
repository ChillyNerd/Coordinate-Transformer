from dash import html, Dash

from src.app.components import BaseComponent
from src.app.components.input.input_angle_form import InputAngleForm
from src.app.components.input.input_numeric_form import InputNumericForm


class InputManualForm(BaseComponent):
    def __init__(self, app: Dash):
        super().__init__(app)
        form = html.Div(
            children=[
                InputNumericForm(self.app).get_layout(),
                InputAngleForm(self.app).get_layout()
            ],
            className="column-gap"
        )
        self.layout = form

    def init_callbacks(self):
        pass
