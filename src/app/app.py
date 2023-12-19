import traceback

from dash import Dash, html, Input, Output, callback
from dash.exceptions import PreventUpdate
from flask import request

from src.app.components import input_form, choose_form, output_form
from src.coordinate_transformer import transform
from src.logger import log

app = Dash(__name__, update_title=None, title='Coordinate Transformer')
data_form = html.Div(children=[input_form, choose_form, output_form], className="row-between data-form")
error_form = html.Div(id='error')
app.layout = html.Div(children=[data_form, error_form], className="column-gap")


@callback(
    Output('lat3_value', 'children'),
    Output('long3_value', 'children'),
    Output('lat4_value', 'children'),
    Output('long4_value', 'children'),
    Output('error', 'children'),
    Input('latitude', 'value'),
    Input('longitude', 'value'),
    Input('projection_from_select', 'value'),
    Input('projection_to_select', 'value')
)
def transform_coordinates(latitude, longitude, projection_from, projection_to):
    if latitude is None or longitude is None or projection_from is None or projection_to is None:
        raise PreventUpdate
    try:
        log.debug(f"{request.remote_addr} is transforming (latitude: {latitude}, longitude: {longitude}) "
                  f"for projections (from: {projection_from}, to: {projection_to})")
        transformed = transform(latitude, longitude, projection_from, projection_to)
        lat3 = transformed['lat3']
        lat4 = transformed['lat4']
        long3 = transformed['long3']
        long4 = transformed['long4']
        log.debug(f"Got {transformed}")
        return str(lat3), str(long3), str(lat4), str(long4), ''
    except Exception as e:
        return None, None, None, None, traceback.format_exc()


@callback(
    Output('projection_from_value', 'children'),
    Input('projection_from_select', 'value')
)
def transform_coordinates(projection_from):
    if projection_from is None:
        raise PreventUpdate
    return projection_from


@callback(
    Output('projection_to_value', 'children'),
    Input('projection_to_select', 'value')
)
def transform_coordinates(projection_to):
    if projection_to is None:
        raise PreventUpdate
    return projection_to
