from dash import html

from src.app.components.output.output_excel_form import form as output_excel_form
from src.app.components.output.output_manual_form import form as output_manual_form

form = html.Div(children=[output_excel_form, output_manual_form], className="column-gap", id='output_form')
