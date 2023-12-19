from dash import dcc, html

input_form_label = html.Div("Input")
latitude_label = html.Div("Enter latitude")
latitude_input = dcc.Input(id='latitude', type='number')
longitude_label = html.Div("Enter longitude")
longitude_input = dcc.Input(id='longitude', type='number')
latitude_form = html.Div(children=[latitude_label, latitude_input], className='row-between')
longitude_form = html.Div(children=[longitude_label, longitude_input], className='row-between')
form = html.Div(children=[input_form_label, latitude_form, longitude_form], className="column-gap input-form")
