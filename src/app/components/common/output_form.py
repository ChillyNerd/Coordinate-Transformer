from dash import html

output_form_label = html.Div("Результат")
lat4_label = html.Div("Широта")
lat4_value = html.Div(id='lat4_value')
lat4_form = html.Div(children=[lat4_label, lat4_value], className='row-between')
long4_label = html.Div("Долгота")
long4_value = html.Div(id='long4_value')
long4_form = html.Div(children=[long4_label, long4_value], className='row-between')
form = html.Div(children=[output_form_label, lat4_form, long4_form],
                className="column-gap output-form")
