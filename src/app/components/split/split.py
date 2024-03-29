import dash_split_pane
from dash import html
from src.app.components.choose_form.choose_form import form as choose_form
from src.app.components.output.output_form import form as output_form
from src.app.components.tabs.tabs import input_tab_form
from src.app.components.input.input_projection_form import projections_to_form

split_pane = dash_split_pane.DashSplitPane(
    children=[
        html.Div(
            children=[choose_form, input_tab_form, projections_to_form, output_form],
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