from dash import html

output_form_label = html.Div("Результат")
output_form_value = html.Div(id='output_excel')
form = html.Div(children=[output_form_label, output_form_value], className="column-gap output-excel-form")
