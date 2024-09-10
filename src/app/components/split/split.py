import dash_split_pane
from dash import html, Dash

from src.app.components import BaseComponent
from src.app.components.choose_form.choose_form import ChooseForm
from src.app.components.output.output_form import OutputForm
from src.app.components.tabs.tabs import Tabs
from src.app.components.input.input_projection_form import ProjectionToForm


class SplitPane(BaseComponent):
    def __init__(self, app: Dash):
        super().__init__(app)
        split_pane = dash_split_pane.DashSplitPane(
            children=[
                html.Div(
                    children=[
                        ChooseForm(self.app).get_layout(),
                        Tabs(self.app).get_layout(),
                        ProjectionToForm(self.app).get_layout(),
                        OutputForm(self.app).get_layout()
                    ],
                    className='column-gap small-padding'
                ),
                html.Iframe(
                    id="map", height="100%", width='100%',
                    style={'padding-left': "10px"}
                )
            ],
            id="splitter",
            split="vertical",
            minSize=400,
            size=600,
            maxSize=800,
            style={'padding': "5px"}
        )
        self.layout = split_pane

    def init_callbacks(self):
        pass
