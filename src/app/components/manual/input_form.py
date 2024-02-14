from dash import html
from src.app.components.manual.input_numeric_form import form as input_numeric_form
from src.app.components.manual.input_angle_form import form as input_angle_form

input_form_label = html.Div("Входные координаты")
form = html.Div(children=[input_form_label, input_numeric_form, input_angle_form], className="column-gap input-form")
