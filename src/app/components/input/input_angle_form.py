from dash import dcc, html

latitude_label = html.Div("Широта")
latitude_angle_input = dcc.Input(id='latitude_angle_input', type='number', className="angle-input-form",
                                 min=-90, max=90, step=1)
latitude_angle_label = html.Div("°")
latitude_angle_minutes_input = dcc.Input(id='latitude_angle_minutes_input', type='number', className="angle-input-form",
                                         min=0, max=60, step=1, value=0)
latitude_angle_minutes_label = html.Div("′")
latitude_angle_seconds_input = dcc.Input(id='latitude_angle_seconds_input', type='number', className="angle-input-form",
                                         min=0, max=60, value=0)
latitude_angle_seconds_label = html.Div("″")
latitude_form_children = [latitude_angle_input, latitude_angle_label, latitude_angle_minutes_input,
                          latitude_angle_minutes_label, latitude_angle_seconds_input, latitude_angle_seconds_label]
latitude_angle_form = html.Div(children=latitude_form_children, className="row-gap")
latitude_form = html.Div(children=[latitude_label, latitude_angle_form], className='row-between')

longitude_label = html.Div("Долгота")
longitude_angle_input = dcc.Input(id='longitude_angle_input', type='number', className="angle-input-form",
                                  min=-180, max=180, step=1)
longitude_angle_label = html.Div("°")
longitude_angle_minutes_input = dcc.Input(id='longitude_angle_minutes_input', type='number',
                                          className="angle-input-form", min=0, max=60, step=1, value=0)
longitude_angle_minutes_label = html.Div("′")
longitude_angle_seconds_input = dcc.Input(id='longitude_angle_seconds_input', type='number',
                                          className="angle-input-form", min=0, max=60, value=0)
longitude_angle_seconds_label = html.Div("″")
longitude_form_children = [longitude_angle_input, longitude_angle_label, longitude_angle_minutes_input,
                           longitude_angle_minutes_label, longitude_angle_seconds_input, longitude_angle_seconds_label]
latitude_angle_form = html.Div(children=longitude_form_children, className="row-gap")
longitude_form = html.Div(children=[longitude_label, latitude_angle_form], className='row-between')

form = html.Div(children=[latitude_form, longitude_form], className='column-gap', id='input_angle_form')
