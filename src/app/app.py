import base64
import logging
import os
import shutil
import traceback

import dash_bootstrap_components as dbc
import folium
from dash import Dash, html, Input, Output, callback, State
from dash.exceptions import PreventUpdate
from flask import Flask, request
from folium.plugins import MarkerCluster
from src.app.components import layout
from src.config import Config
from src.coordinate_transformer import (projections_dict, CoordinateTransformer, BaseTransformException, Metrics)


class ApplicationServer:
    def __init__(self, config: Config):
        self.config = config
        self.log = logging.getLogger(config.application_server)
        self.app = Dash(__name__, update_title=None, title='Калькулятор координат',
                        external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.hidden = 'component-hidden'
        self.app.layout = layout
        self.init_callbacks()

    def init_callbacks(self):
        @self.app.server.route('/client-close', methods=['POST'])
        def handle_client_close():
            client = request.remote_addr
            self.log.debug(f"Client {client} has closed application")
            self.delete_clients_repo(client)
            return '', 200

        @callback(
            Output('error', 'children'),
            Input('transform_error', 'data'),
            Input('excel_upload_error', 'data'),
            Input('excel_read_error', 'data')
        )
        def set_error(transform_error, excel_upload_error, excel_read_error):
            errors = []
            if transform_error is not None:
                errors.append(transform_error)
            if excel_upload_error is not None:
                errors.append(excel_upload_error)
            if excel_read_error is not None:
                errors.append(excel_read_error)
            if len(errors) == 0:
                return None
            return list(map(lambda error: html.Div(error), errors))

        @callback(
            [
                Output('result_latitude', 'children'),
                Output('result_longitude', 'children'),
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
                from_, to_ = projections_dict[projection_from], projections_dict[projection_to]
                transformer = CoordinateTransformer(from_, to_)
                result_latitude, result_longitude = transformer.transform(latitude, longitude)
                from_string = f'{latitude, longitude} {from_.comment} ({projection_from})'
                to_string = f'{result_latitude, result_longitude} {to_.comment} ({projection_to})'
                self.log.info(f"{request.remote_addr} transformed from {from_string} to {to_string}")
                return str(result_latitude), str(result_longitude), ''
            except BaseTransformException as e:
                self.log.error(e.message)
                return None, None, e.message
            except Exception as e:
                self.log.exception(e)
                return None, None, traceback.format_exc()

        @callback(
            [
                Output('output-manual-form', 'className')
            ], [
                Input('result_latitude', 'children'),
                Input('result_longitude', 'children'),
                Input('tabs_select', 'active_tab'),
                State('output-manual-form', 'className')
            ]
        )
        def show_manual_result(result_latitude, result_longitude, active_tab, class_names):
            classes = class_names.split()
            if result_latitude is None or result_longitude is None or active_tab != 'manual_tab':
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]

        @callback(
            [
                Output('projection_from_select', 'options'),
                Output('projection_from_select', 'value'),
                Output('input_angle_form', 'className'),
                Output('input_numeric_form', 'className')
            ], [
                Input('metrics_select', 'value'),
                State('input_angle_form', 'className'),
                State('input_numeric_form', 'className'),
            ]
        )
        def select_input_form(metric, angle_class_name, numeric_class_name):
            if metric is None:
                raise PreventUpdate
            angle_classes = angle_class_name.split()
            numeric_classes = numeric_class_name.split()
            projections = projections_dict.values()
            projections_from = list(filter(
                lambda projection: metric in projection.allowed_metrics and not projection.disabled, projections
            ))
            projections_from_options = [{'label': proj.comment, 'value': proj.mnemonic} for proj in projections_from]
            if metric == Metrics.METER.name or metric == Metrics.FLOAT_ANGLE.name:
                if self.hidden not in angle_classes:
                    angle_classes.append(self.hidden)
                if self.hidden in numeric_classes:
                    numeric_classes = list(filter(lambda class_name: class_name != self.hidden, numeric_classes))
            if metric == Metrics.ANGLE.name:
                if self.hidden in angle_classes:
                    angle_classes = list(filter(lambda class_name: class_name != self.hidden, angle_classes))
                if self.hidden not in numeric_classes:
                    numeric_classes.append(self.hidden)
            return projections_from_options, None, ' '.join(angle_classes), ' '.join(numeric_classes)

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
                return [angle + minutes / 60.0 + seconds / 3600.0]
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

        @callback([
            Output('excel_file', 'data'),
            Output('excel_file_name', 'children'),
            Output('excel_upload_error', 'data')
        ], [
            Input('upload_excel_file', 'contents'),
            State('upload_excel_file', 'filename')
        ])
        def upload_excel_file(file_content, file_name):
            if not file_name:
                return None, 'Выберите файл', None
            try:
                file = {'filename': file_name, 'content': file_content}
                path = self.save_excel_file(request.remote_addr, file)
                self.log.info(f'{request.remote_addr} successfully uploaded excel file {file_name}')
                return path, file_name, None
            except Exception as ex:
                self.log.exception(ex)
                return None, 'Выберите файл', traceback.format_exc()

        @callback(
            [
                Output('upload_excel_file', 'contents'),
                Output('upload_excel_file', 'filename')
            ], [
                Input('delete_excel_file', 'n_clicks')
            ])
        def clear_excel_file(clicks):
            if clicks:
                self.delete_files(request.remote_addr, 'excel_input')
                return None, None
            else:
                raise PreventUpdate

        @callback([
            Output('output_manual_form', 'className')
        ], [
            Input('excel_file', 'data'),
            Input('tabs_select', 'active_tab'),
            Input('projection_from_select', 'value'),
            Input('projection_to_select', 'value'),
            State('output_manual_form', 'className')
        ]
        )
        def show_excel_file(excel_file, active_tab, projection_from, projection_to, output_classes):
            classes = output_classes.split()
            if excel_file is None or projection_from is None or projection_to is None or active_tab != 'excel_tab':
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]

        @callback(
            Output('excel_points', 'data'),
            Output('excel_read_error', 'data'),
            Input('excel_file', 'data'),
            Input('projection_from_select', 'value'),
        )
        def read_excel(excel_file, projection_from):
            if excel_file is None:
                return [], None
            try:
                transformer = CoordinateTransformer(projections_dict[projection_from], projections_dict["epsg:4326"])
                return transformer.transform_excel(excel_file), None
            except BaseTransformException as ex:
                self.log.exception(ex)
                return [], ex.message
            except Exception as ex:
                self.log.exception(ex)
                return [], traceback.format_exc()

        @callback(
            [
                Output('manual_points', 'data'),
            ], [
                Input('latitude', 'data'),
                Input('longitude', 'data'),
                Input('projection_from_select', 'value'),
                Input('tabs_select', 'active_tab'),
            ]
        )
        def set_manual_points(latitude, longitude, projection_from, selected_tab):
            points = []
            try:
                if latitude is None or longitude is None or projection_from is None or selected_tab != 'manual_tab':
                    return [points]
                transformer = CoordinateTransformer(projections_dict[projection_from], projections_dict["epsg:4326"])
                correct_latitude, correct_longitude = transformer.transform(latitude, longitude)
                point = {'latitude': correct_latitude, 'longitude': correct_longitude, 'id': 1}
                points.append(point)
                return [points]
            except Exception as e:
                self.log.exception(e)
                print(traceback.format_exc())
                return [points]

        @callback(
            Output('points', 'data'),
            Input('manual_points', 'data'),
            Input('excel_points', 'data'),
            State('tabs_select', 'active_tab')
        )
        def set_points(manual_points, excel_points, selected_tab):
            if selected_tab == 'manual_tab':
                return manual_points
            if selected_tab == 'excel_tab':
                return excel_points
            return []

        @callback(
            Output('map', 'srcDoc'),
            Input('points', 'data')
        )
        def set_map(points):
            if points is None:
                points = []
            map_frame = folium.Map(location=[0, 0], zoom_start=2)
            marker_cluster = MarkerCluster().add_to(map_frame)
            for point in points:
                folium.Marker(
                    location=[point['latitude'], point['longitude']],
                    popup=f'{point["id"]}',
                    icon=folium.Icon(color="blue")
                ).add_to(marker_cluster)
            # TODO Придумать как возвращать карту не через этот метод
            return map_frame._repr_html_()

        @callback(
            [
                Output('input_tabs', 'className')
            ], [
                Input('metrics_select', 'value'),
                Input('projection_from_select', 'value'),
                State('input_tabs', 'className')
            ]
        )
        def show_input_form(selected_metric, selected_projection, tabs_classes):
            classes = tabs_classes.split()
            if selected_metric is None or selected_projection is None:
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]

        @callback(
            [
                Output('projection-to-form', 'className')
            ], [
                Input('points', 'data'),
                State('projection-to-form', 'className')
            ]
        )
        def show_projection_to_form(points, projection_classes):
            classes = projection_classes.split()
            if points is None or len(points) == 0:
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]

    def save_excel_file(self, client_address, file: dict):
        directory_path = self.refresh_or_create_directory(client_address, 'excel_input')
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

    def delete_clients_repo(self, client_address):
        client_path = os.path.join(self.config.files_path, client_address)
        if os.path.exists(client_path):
            shutil.rmtree(client_path)

    def delete_files(self, client_address, file_type):
        client_path = os.path.join(self.config.files_path, client_address)
        if os.path.exists(client_path):
            files_path = os.path.join(client_path, file_type)
            if os.path.exists(files_path):
                content = os.listdir(files_path)
                for file in content:
                    os.remove(os.path.join(files_path, file))
                os.rmdir(files_path)
