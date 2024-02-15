from dash import html

from src.app.components.input.input_angle_form import form as input_angle_form
from src.app.components.input.input_numeric_form import form as input_numeric_form

form = html.Div(children=[input_numeric_form, input_angle_form], className="column-gap")
