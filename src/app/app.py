import base64
import logging
import os
import traceback
import geopandas
import dash_bootstrap_components as dbc
import folium
from dash import Dash, Input, Output, callback, State, dcc
from dash.exceptions import PreventUpdate
from flask import request
from folium.plugins import MarkerCluster
from src.app.components import layout
from src.config import Config
from src.coordinate_transformer.coordinate_formater import format_coordinate, angle_to_float
from src.coordinate_transformer import projections_dict, CoordinateTransformer, BaseTransformException
from src.coordinate_transformer.enums import OutputMetrics, Metrics
from src.excel_transformer import ExcelTransformer, BaseExcelTransformException
from src.shape_reader import ShapeReader, BaseShapeReadException


class ApplicationServer:
    def __init__(self, config: Config):
        self.config = config
        self.log = logging.getLogger(config.application_server)
        self.app = Dash(__name__, update_title=None, title='Калькулятор координат',
                        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
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

        @callback([
            Output('error', 'children'),
            Output('error', 'is_open')
        ], [
            Input('transform_error', 'data'),
            Input('excel_upload_error', 'data'),
            Input('excel_show_error', 'data'),
            Input('excel_read_error', 'data'),
            Input('shape_read_error', 'data')
        ])
        def set_error(transform_error, excel_upload_error, excel_show_error, excel_read_error, shape_read_error):
            errors = []
            if transform_error is not None:
                errors.append(transform_error)
            if excel_upload_error is not None:
                errors.append(excel_upload_error)
            if excel_read_error is not None:
                errors.append(excel_read_error)
            if excel_show_error is not None:
                errors.append(excel_show_error)
            if shape_read_error is not None:
                errors.append(shape_read_error)
            if len(errors) == 0:
                return None, False
            return '\n'.join(errors), True

        @callback(
            [
                Output('result_latitude', 'children'),
                Output('result_longitude', 'children'),
                Output('transform_error', 'data')
            ], [
                Input('latitude', 'data'),
                Input('longitude', 'data'),
                Input('zone_from_select', 'value'),
                Input('zone_to_select', 'value'),
                Input('output_metrics_select', 'value')
            ]
        )
        def transform_coordinates(latitude, longitude, projection_from, projection_to, output_metric):
            if latitude is None or longitude is None or projection_from is None or projection_to is None:
                return None, None, None
            try:
                from_, to_ = projections_dict[projection_from], projections_dict[projection_to]
                transformer = CoordinateTransformer(from_, to_)
                result_latitude, result_longitude = transformer.transform(latitude, longitude)
                from_string = f'{latitude, longitude} {from_.comment} ({projection_from})'
                to_string = f'{result_latitude, result_longitude} {to_.comment} ({projection_to})'
                self.log.info(f"{request.remote_addr} transformed from {from_string} to {to_string}")
                return format_coordinate(coordinate=result_latitude, metric=output_metric), format_coordinate(coordinate=result_longitude, metric=output_metric), None
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
                Output('zone_from_select', 'options'),
                Output('zone_from_select', 'value'),
                Output('input_angle_form', 'className'),
                Output('input_numeric_form', 'className')
            ], [
                Input('metrics_select', 'value'),
                Input('projection_from_select', 'value'),
                State('input_angle_form', 'className'),
                State('input_numeric_form', 'className'),
            ]
        )
        def select_input_form(metric_name, projection_from, angle_class_name, numeric_class_name):
            if metric_name is None:
                raise PreventUpdate
            angle_classes = angle_class_name.split()
            numeric_classes = numeric_class_name.split()
            projections = projections_dict.values()
            zones_from = list(filter(
                lambda projection: metric_name in [metric.name for metric in Metrics if metric.value.metric_type == projection.metric_type] and not projection.disabled and projection.projection_group == projection_from, projections
            ))
            projections_from_options = [{'label': proj.comment, 'value': proj.mnemonic} for proj in zones_from]
            if metric_name == Metrics.METER.name or metric_name == Metrics.FLOAT_ANGLE.name:
                if self.hidden not in angle_classes:
                    angle_classes.append(self.hidden)
                if self.hidden in numeric_classes:
                    numeric_classes = list(filter(lambda class_name: class_name != self.hidden, numeric_classes))
            if metric_name == Metrics.ANGLE.name:
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
            Output('zone_to_select', 'options'),
            Output('zone_to_select', 'value'),
            Input('projection_to_select', 'value')
        )
        def filter_zones(group_name):
            projections = list(filter(lambda projection: projection.projection_group == group_name, projections_dict.values()))
            return [{'label': projection.comment, 'value': projection.mnemonic} for projection in projections], None
        
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
                return [angle_to_float(angle, minutes, seconds)]
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
                return [angle_to_float(angle, minutes, seconds)]
            return [None]

        @callback(
            Output('output_metrics_select', 'options'),
            Output('output_metrics_select', 'value'),
            Input('zone_to_select', 'value'),
        )
        def set_output_metrics(zone_name):
            if zone_name is None:
                raise PreventUpdate
            zone_to = projections_dict[zone_name]
            allowed_metrics = [{'label': metric.value.label, 'value': metric.name} for metric in OutputMetrics if metric.value.metric_type == zone_to.metric_type]
            return allowed_metrics, allowed_metrics[0]['value']

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
                path = self.upload_file(request.remote_addr, 'excel_input', file)
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
            Input('excel_points', 'data'),
            Input('tabs_select', 'active_tab'),
            Input('zone_from_select', 'value'),
            Input('zone_to_select', 'value'),
            State('output_manual_form', 'className')
        ]
        )
        def show_excel_file(excel_points, active_tab, projection_from, projection_to, output_classes):
            classes = output_classes.split()
            if excel_points is None or projection_from is None or projection_to is None or active_tab != 'excel_tab':
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]

        @callback([
            Output('zone_to_form', 'className')
        ], [
            Input('points', 'data'),
            Input('projection_to_select', 'value'),
            State('zone_to_form', 'className')
        ]
        )
        def show_zone_select_form(points, projection_group, output_classes):
            classes = output_classes.split()
            if projection_group is None or points is None or len(points) == 0:
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]

        @callback(
            Output('excel_columns', 'data'),
            Output('excel_read_error', 'data'),
            Input('excel_file', 'data'),
        )
        def read_excel(excel_file):
            if excel_file is None:
                return None, None
            try:
                return ExcelTransformer.get_excel_columns(excel_file), None
            except BaseExcelTransformException as ex:
                self.log.exception(ex)
                return None, ex.message
            except Exception as ex:
                self.log.exception(ex)
                return None, traceback.format_exc()

        @callback([
            Output('shape_archive', 'data'),
            Output('shape_file_name', 'children'),
            Output('shape_upload_error', 'data')
        ], [
            Input('upload_shape_file', 'contents'),
            State('upload_shape_file', 'filename')
        ])
        def upload_shape_file(file_content, file_name):
            if not file_name:
                return None, 'Выберите файл', None
            try:
                file = {'filename': file_name, 'content': file_content}
                path = self.upload_file(request.remote_addr, 'shape_input', file)
                self.log.info(f'{request.remote_addr} successfully uploaded shape file {file_name}')
                return path, file_name, None
            except Exception as ex:
                self.log.exception(ex)
                return None, 'Выберите файл', traceback.format_exc()

        @callback([
            Output('upload_shape_file', 'contents'),
            Output('upload_shape_file', 'filename')
        ], [
            Input('delete_shape_file', 'n_clicks')
        ])
        def clear_shape_file(clicks):
            if clicks:
                self.delete_files(request.remote_addr, 'shape_input')
                return None, None
            else:
                raise PreventUpdate

        @callback(
            Output('shape_files', 'data'),
            Output('shape_read_error', 'data'),
            Input('shape_archive', 'data')
        )
        def read_shape(shape_archive):
            if shape_archive is None:
                return None, None
            try:
                return ShapeReader.read(shape_archive), None
            except BaseShapeReadException as ex:
                self.log.exception(ex)
                return None, ex.message
            except Exception as ex:
                self.log.exception(ex)
                return None, traceback.format_exc()

        @callback(
            Output('longitude_column_select', 'options'),
            Output('latitude_column_select', 'options'),
            Input('excel_columns', 'data'),
        )
        def set_column_options(columns):
            if columns is None:
                return None, None
            options = [{'label': column, 'value': index} for index, column in enumerate(columns)]
            return options, options

        @callback(
            Output('latitude_column_select', 'value'),
            Input('latitude_column_select', 'options'),
        )
        def null_latitude_column_value(latitude_select):
            return None

        @callback(
            Output('longitude_column_select', 'value'),
            Input('longitude_column_select', 'options'),
        )
        def null_longitude_column_value(longitude_select):
            return None

        @callback([
            Output('excel_points', 'data'),
            Output('excel_show_error', 'data')
        ], [
            Input('confirm_columns', 'n_clicks'),
            Input('zone_from_select', 'value'),
            Input('latitude_column_select', 'value'),
            Input('longitude_column_select', 'value'),
            State('excel_file', 'data'),
            State('metrics_select', 'value')
        ])
        def set_excel_points(confirm_clicks, projection_from, latitude_column, longitude_column, excel_file, metric):
            if excel_file is None or projection_from is None or latitude_column is None or longitude_column is None:
                return None, None
            try:
                transformer = ExcelTransformer(
                    projection_from=projections_dict[projection_from],
                    projection_to=projections_dict["epsg:4326"],
                    latitude_column=int(latitude_column),
                    longitude_column=int(longitude_column),
                    metric=metric
                )
                points = []
                df = transformer.transform(excel_file)
                for index in range(len(df)):
                    row = df.iloc[index]
                    points.append({'latitude': row['result_latitude'], 'longitude': row['result_longitude'], 'id': index})
                return points, None
            except BaseExcelTransformException as ex:
                self.log.exception(ex)
                return None, ex.message
            except Exception as ex:
                self.log.exception(ex)
                return None, traceback.format_exc()

        @callback(
            Output('choose_column_dialog', 'is_open'),
            Input('toggle_choose_column_dialog', 'data'),
            Input('inspect_excel_file', 'n_clicks'),
            Input('confirm_columns', 'n_clicks'),
            State('choose_column_dialog', 'is_open')
        )
        def toggle_choose_column_dialog(toggle, inspect_clicks, delete_clicks, is_open):
            if toggle is None or not toggle:
                raise PreventUpdate
            is_open = not is_open
            return is_open

        @callback(
            Output('toggle_choose_column_dialog', 'data'),
            Input('excel_columns', 'data')
        )
        def choose_columns(columns):
            if columns is None:
                return False
            return True

        @callback(
            [
                Output('manual_points', 'data'),
            ], [
                Input('latitude', 'data'),
                Input('longitude', 'data'),
                Input('zone_from_select', 'value'),
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
            Input('points', 'data'),
            Input('shape_files', 'data'),
            State('tabs_select', 'active_tab')
        )
        def set_map(points, shape_files, active_tab):
            if points is None:
                points = []
            map_frame = folium.Map(location=[62, 75], zoom_start=4)
            if active_tab == 'shape_tab' and shape_files is not None:
                for file in shape_files:
                    geo_file = geopandas.read_file(file)
                    folium.GeoJson(geo_file, popup=os.path.basename(file)).add_to(map_frame)
            else:
                marker_cluster = MarkerCluster().add_to(map_frame)
                for point in points:
                    folium.Marker(
                        location=[point['latitude'], point['longitude']],
                        popup=f'{point["id"]}',
                        icon=folium.Icon(color="blue")
                    ).add_to(marker_cluster)
            return map_frame.get_root().render()

        @callback(
            [
                Output('input_tabs', 'className')
            ], [
                Input('metrics_select', 'value'),
                Input('zone_from_select', 'value'),
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
                Output('projection_to_form', 'className')
            ], [
                Input('points', 'data'),
                State('projection_to_form', 'className')
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

        @callback(
            Output('download_data', 'data'),
            Input('download_excel_file', 'n_clicks'),
            State('zone_from_select', 'value'),
            State('zone_to_select', 'value'),
            State('latitude_column_select', 'value'),
            State('longitude_column_select', 'value'),
            State('upload_excel_file', 'filename'),
            State('excel_file', 'data'),
            State('metrics_select', 'value'),
        )
        def download_excel_file(clicks, projection_from, projection_to, latitude_column, longitude_column, file_name, excel_file, metric):
            if clicks:
                name_without_ext = os.path.splitext(file_name)[0]
                result_filename = f'{name_without_ext}-{projections_dict[projection_to].comment}.xlsx'
                transformator = ExcelTransformer(
                    projection_from=projections_dict[projection_from],
                    projection_to=projections_dict[projection_to],
                    latitude_column=int(latitude_column),
                    longitude_column=int(longitude_column),
                    metric=metric
                )
                df = transformator.transform(excel_file)
                return dcc.send_data_frame(df.to_excel, result_filename, sheet_name='Sheet1', index=None)
            raise PreventUpdate

    def upload_file(self, client_address, file_type: str, file: dict):
        directory_path = self.refresh_or_create_directory(client_address, file_type)
        return self.save_file(directory_path, file['filename'], file['content'])

    def refresh_or_create_directory(self, client_address, file_type: str):
        clients_path = os.path.join(self.config.files_path, client_address)
        if not os.path.exists(clients_path):
            os.mkdir(clients_path)
        file_path = os.path.join(clients_path, file_type)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        content = os.listdir(file_path)
        for file in content:
            self.recursive_files_delete(os.path.join(file_path, file))
        return file_path

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
            self.recursive_files_delete(client_path)
            self.log.info(f'Removed {client_address} directory')

    def delete_files(self, client_address, file_type):
        client_path = os.path.join(self.config.files_path, client_address)
        if not os.path.exists(client_path):
            return
        self.recursive_files_delete(os.path.join(client_path, file_type))
        self.log.info(f'Removed {client_address} {file_type} directory')

    def recursive_files_delete(self, filepath):
        if not os.path.exists(filepath):
            return
        if os.path.isdir(filepath):
            content = os.listdir(filepath)
            for file in content:
                self.recursive_files_delete(os.path.join(filepath, file))
            os.rmdir(filepath)
        else:
            os.remove(filepath)
