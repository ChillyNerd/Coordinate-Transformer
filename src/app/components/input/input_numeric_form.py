from dash import dcc, html

latitude_label = html.Div("Широта", className='common-label')
latitude_input = dcc.Input(id='latitude_numeric_input', type='number', className="common-input")
latitude_form = html.Div(children=[latitude_label, latitude_input], className='row-between')
longitude_label = html.Div("Долгота", className='common-label')
longitude_input = dcc.Input(id='longitude_numeric_input', type='number', className="common-input")
longitude_form = html.Div(children=[longitude_label, longitude_input], className='row-between')

form = html.Div(children=[latitude_form, longitude_form], className='column-gap', id='input_numeric_form')
