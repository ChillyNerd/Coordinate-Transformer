from dash import html, Dash

from src.app.components import BaseComponent
from src.app.components.output.output_excel_form import OutputExcelForm
from src.app.components.output.output_manual_form import OutputManualForm
from src.app.components.output.output_shape_form import OutputShapeForm


class OutputForm(BaseComponent):
    def __init__(self, app: Dash):
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

    def init_callbacks(self):
        pass
