import base64
import os
import traceback

import folium
from dash import Dash, html, Input, Output, callback, State, dcc
from dash.exceptions import PreventUpdate
from flask import request
from folium.plugins import MarkerCluster

from src.app.components import *
from src.config import Config
from src.coordinate_transformer import BaseTransformException, Metrics, projections, trans, trans_excel
from src.logger import log


class ApplicationServer:
    def __init__(self, config: Config):
        self.config = config
        self.app = Dash(__name__, update_title=None, title='Калькулятор координат')
        common_form = html.Div(children=[input_form, choose_form, output_form], className="row-between common-form")
        file_form = html.Div(children=[input_excel_form, output_excel_form], className="row-between file-form")
        map_form = html.Iframe(id="map", width="1300", height="700")
        error_form = html.Div(id='error', className='column-gap')
        self.app.layout = html.Div(
            children=[
                dcc.Store(id='latitude'),
                dcc.Store(id='longitude'),
                dcc.Store(id='numeric_latitude'),
                dcc.Store(id='numeric_longitude'),
                dcc.Store(id='angle_latitude'),
                dcc.Store(id='angle_longitude'),
                dcc.Store(id='excel_file'),
                dcc.Store(id='transform_error'),
                dcc.Store(id='excel_upload_error'),
                common_form,
                file_form,
                map_form,
                error_form
            ],
            className="column-gap"
        )
        self.init_callbacks()

    def init_callbacks(self):
        @callback(
            Output('error', 'children'),
            Input('transform_error', 'data'),
            Input('excel_upload_error', 'data')
        )
        def set_error(transform_error, excel_upload_error):
            errors = []
            if transform_error is not None:
                errors.append(transform_error)
            if excel_upload_error is not None:
                errors.append(excel_upload_error)
            if len(errors) == 0:
                return None
            return list(map(lambda error: html.Div(error), errors))

        @callback(
            [
                Output('lat4_value', 'children'),
                Output('long4_value', 'children'),
                Output('transform_error', 'data')
            ], [
                Input('latitude', 'data'),
                Input('longitude', 'data'),
                Input('projection_from_select', 'value'),
                Input('projection_to_select', 'value')
            ]
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
            Output('output_excel', 'children'),
            Input('excel_file', 'data')
        )
        def read_excel(excel_file):
            if excel_file is None:
                return None
            return trans_excel(excel_file)

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
            [
                Output('input_form', 'children'),
                Output('projection_from_select', 'options'),
                Output('projection_from_select', 'value')
            ], [
                Input('metrics_select', 'value')
            ]
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
            [
                Output('angle_longitude', 'data')
            ], [
                Input('longitude_angle_input', 'value'),
                Input('longitude_angle_minutes_input', 'value'),
                Input('longitude_angle_seconds_input', 'value'),
                Input('metrics_select', 'value')
            ]
        )
        def set_angle_longitude(angle, minutes, seconds, metric):
            if metric == Metrics.METER.name or metric == Metrics.FLOAT_ANGLE.name:
                return [None]
            if angle is not None and minutes is not None and seconds is not None:
                return [angle + minutes / 60.0 + seconds / 3600.0]
            return [None]

        @callback(
            [
                Output('angle_latitude', 'data')
            ], [
                Input('latitude_angle_input', 'value'),
                Input('latitude_angle_minutes_input', 'value'),
                Input('latitude_angle_seconds_input', 'value'),
                Input('metrics_select', 'value')
            ]
        )
        def set_angle_latitude(angle, minutes, seconds, metric):
            if metric == Metrics.METER.name or metric == Metrics.FLOAT_ANGLE.name:
                return [None]
            if angle is not None and minutes is not None and seconds is not None:
                return [angle + minutes/60.0 + seconds/3600.0]
            return [None]

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
            [
                Output('latitude_numeric_input', 'min'),
                Output('latitude_numeric_input', 'max'),
                Output('longitude_numeric_input', 'min'),
                Output('longitude_numeric_input', 'max')
            ], [
                Input('metrics_select', 'value')
            ]
        )
        def set_input_limit(metric):
            if metric == Metrics.FLOAT_ANGLE.name:
                return -90, 90, -180, 180
            return None, None, None, None

        @callback(
            Output('excel_file', 'data'),
            Output('excel_upload_error', 'data'),
            Input('upload_excel_file', 'contents'),
            State('upload_excel_file', 'filename')
        )
        def upload_excel_file(file_content, file_name):
            if not file_name:
                return None, None
            try:
                file = {'filename': file_name, 'content': file_content}
                path = self.save_excel_file(request.remote_addr, file)
                log.debug(f'{request.remote_addr} successfully uploaded excel file {file_name}')
                return path, None
            except Exception as ex:
                log.exception(ex)
                return None, traceback.format_exc()

        @callback(
            [
                Output('map', 'srcDoc'),
            ], [
                Input('latitude', 'data'),
                Input('longitude', 'data'),
                Input('projection_from_select', 'value'),
            ]
        )
        def set_map(latitude, longitude, projection_from):
            try:
                if latitude is None or longitude is None or projection_from is None or projection_from != "epsg:4284":
                    return [None]
                correct_latitude, correct_longitude = trans(latitude, longitude, projection_from, "epsg:4326")
                map_frame = folium.Map(location=[0, 0], zoom_start=3)
                marker_cluster = MarkerCluster().add_to(map_frame)
                folium.Marker(
                    location=[correct_latitude, correct_longitude],
                    popup='Point',
                    icon=folium.Icon(color="blue")
                ).add_to(marker_cluster)
                return [map_frame._repr_html_()]
            except Exception as e:
                print(traceback.format_exc())
                return [None]

    def save_excel_file(self, client_address, file: dict):
        directory_path = self.refresh_or_create_directory(client_address, 'excel')
        return self.save_file(directory_path, file['filename'], file['content'])

    def refresh_or_create_directory(self, client_address, file_type: str):
        path = os.path.join(self.config.files_path, client_address)
        if not os.path.exists(path):
            os.mkdir(path)
        path = os.path.join(path, file_type)
        if not os.path.exists(path):
            os.mkdir(path)
        content = os.listdir(path)
        for file in content:
            os.remove(os.path.join(path, file))
        return path

    @staticmethod
    def save_file(path, name, content):
        data = content.encode("utf8").split(b";base64,")[1]
        file_path = os.path.join(path, name)
        with open(file_path, "wb") as fp:
            fp.write(base64.decodebytes(data))
        return file_path
