from dash import html

output_form_label = html.Div("Результат")
result_latitude_label = html.Div("Широта", className='label-form')
result_latitude_value = html.Div(id='result_latitude')
result_latitude_form = html.Div(children=[result_latitude_label, result_latitude_value], className='row-between')
result_longitude_label = html.Div("Долгота", className='label-form')
result_longitude_value = html.Div(id='result_longitude')
result_longitude_form = html.Div(children=[result_longitude_label, result_longitude_value], className='row-between')
form = html.Div(children=[output_form_label, result_latitude_form, result_longitude_form],
                className="column-gap output-form", id='manual-output-form')
