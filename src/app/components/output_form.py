from dash import html

output_form_label = html.Div("Output")
lat3_label = html.Div("Lat3")
lat3_value = html.Div(id='lat3_value')
lat3_form = html.Div(children=[lat3_label, lat3_value], className='row-between')
long3_label = html.Div("Long3")
long3_value = html.Div(id='long3_value')
long3_form = html.Div(children=[long3_label, long3_value], className='row-between')
lat4_label = html.Div("Lat4")
lat4_value = html.Div(id='lat4_value')
lat4_form = html.Div(children=[lat4_label, lat4_value], className='row-between')
long4_label = html.Div("Long4")
long4_value = html.Div(id='long4_value')
long4_form = html.Div(children=[long4_label, long4_value], className='row-between')
form = html.Div(children=[output_form_label, lat3_form, long3_form, lat4_form, long4_form],
                className="column-gap output-form")
