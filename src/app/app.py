import traceback

from dash import Dash, html, Input, Output, callback, State, dcc
from dash.exceptions import PreventUpdate
from flask import request

from src.app.components import input_form, choose_form, output_form, input_angle_form, input_numeric_form
from src.coordinate_transformer import BaseTransformException, Metrics, projections, trans
from src.logger import log

app = Dash(__name__, update_title=None, title='Калькулятор координат')
data_form = html.Div(children=[input_form, choose_form, output_form], className="row-between data-form")
error_form = html.Div(id='error')
app.layout = html.Div(
    children=[
        dcc.Store(id='latitude'),
        dcc.Store(id='longitude'),
        dcc.Store(id='numeric_latitude'),
        dcc.Store(id='numeric_longitude'),
        dcc.Store(id='angle_latitude'),
        dcc.Store(id='angle_longitude'),
        data_form,
        error_form
    ],
    className="column-gap"
)


@callback(
    Output('lat4_value', 'children'),
    Output('long4_value', 'children'),
    Output('error', 'children'),
    Input('latitude', 'data'),
    Input('longitude', 'data'),
    Input('projection_from_select', 'value'),
    Input('projection_to_select', 'value')
)
def transform_coordinates(latitude, longitude, projection_from, projection_to):
    if latitude is None or longitude is None or projection_from is None or projection_to is None:
        return None, None, None
    try:
        log.debug(f"{request.remote_addr} is transforming (latitude: {latitude}, longitude: {longitude}) "
                  f"for projections (from: {projection_from}, to: {projection_to})")
        lat4, long4 = trans(latitude, longitude, projection_from, projection_to)
        log.debug(f"Got {lat4, long4}")
        return str(lat4), str(long4), ''
    except BaseTransformException as e:
        log.error(e.message)
        return None, None, e.message
    except Exception as e:
        log.exception(e)
        return None, None, traceback.format_exc()


@callback(
    Output('projection_from_value', 'children'),
    Input('projection_from_select', 'value')
)
def select_projection_from(projection_from):
    return projection_from


@callback(
    Output('projection_to_value', 'children'),
    Input('projection_to_select', 'value')
)
def select_projection_to(projection_to):
    return projection_to


@callback(
    Output('input_form', 'children'),
    Output('projection_from_select', 'options'),
    Output('projection_from_select', 'value'),
    Input('metrics_select', 'value')
)
def select_input_form(metric):
    if metric is None:
        raise PreventUpdate
    projections_from = list(filter(lambda projection: metric in projection.allowed_metrics, projections))
    projections_from_options = [{'label': proj.comment, 'value': proj.mnemonic} for proj in projections_from]
    if metric == Metrics.METER.name or metric == Metrics.FLOAT_ANGLE.name:
        return input_numeric_form, projections_from_options, None
    if metric == Metrics.ANGLE.name:
        return input_angle_form, projections_from_options, None
    raise PreventUpdate


@callback(
    Output('numeric_longitude', 'data'),
    Input('longitude_numeric_input', 'value'),
    Input('metrics_select', 'value')
)
def set_numeric_longitude(longitude, metric):
    if metric == Metrics.ANGLE.name:
        return None
    return longitude


@callback(
    Output('numeric_latitude', 'data'),
    Input('latitude_numeric_input', 'value'),
    Input('metrics_select', 'value')
)
def set_numeric_latitude(latitude, metric):
    if metric == Metrics.ANGLE.name:
        return None
    return latitude


@callback(
    Output('angle_longitude', 'data'),
    Input('longitude_angle_input', 'value'),
    Input('longitude_angle_minutes_input', 'value'),
    Input('longitude_angle_seconds_input', 'value'),
    Input('metrics_select', 'value')
)
def set_angle_longitude(angle, minutes, seconds, metric):
    if metric == Metrics.METER.name or metric == Metrics.FLOAT_ANGLE.name:
        return None
    if angle is not None and minutes is not None and seconds is not None:
        return angle + minutes / 60.0 + seconds / 3600.0
    return None


@callback(
    Output('angle_latitude', 'data'),
    Input('latitude_angle_input', 'value'),
    Input('latitude_angle_minutes_input', 'value'),
    Input('latitude_angle_seconds_input', 'value'),
    Input('metrics_select', 'value')
)
def set_angle_latitude(angle, minutes, seconds, metric):
    if metric == Metrics.METER.name or metric == Metrics.FLOAT_ANGLE.name:
        return None
    if angle is not None and minutes is not None and seconds is not None:
        return angle + minutes/60.0 + seconds/3600.0
    return None


@callback(
    Output('latitude', 'data'),
    Input('angle_latitude', 'data'),
    Input('numeric_latitude', 'data'),
)
def set_latitude(angle, numeric):
    if angle is None and numeric is None:
        return None
    if angle is not None and numeric is not None:
        return None
    if angle is None:
        return numeric
    else:
        return angle


@callback(
    Output('longitude', 'data'),
    Input('angle_longitude', 'data'),
    Input('numeric_longitude', 'data'),
)
def set_longitude(angle, numeric):
    if angle is None and numeric is None:
        return None
    if angle is not None and numeric is not None:
        return None
    if angle is None:
        return numeric
    else:
        return angle


@callback(
    Output('latitude_numeric_input', 'min'),
    Output('latitude_numeric_input', 'max'),
    Output('longitude_numeric_input', 'min'),
    Output('longitude_numeric_input', 'max'),
    Input('metrics_select', 'value')
)
def set_input_limit(metric):
    if metric == Metrics.FLOAT_ANGLE.name:
        return -90, 90, -180, 180
    return None, None, None, None
