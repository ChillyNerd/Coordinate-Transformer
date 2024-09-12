import traceback

from dash import html, Output, Input
from flask import request

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.app.components.input.input_angle_form import InputAngleForm
from src.app.components.input.input_numeric_form import InputNumericForm
from src.coordinate_transformer import CoordinateTransformer, projections_dict, BaseTransformException
from src.coordinate_transformer.coordinate_formater import format_coordinate


class InputManualForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        form = html.Div(
            children=[
                InputNumericForm(self.app).get_layout(),
                InputAngleForm(self.app).get_layout()
            ],
            className="column-gap"
        )
        self.layout = form
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback(
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

        @self.dash_app.callback(
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

        @self.dash_app.callback(
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
                self.app.log.exception(e)
                return [points]

        @self.dash_app.callback(
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
                self.app.log.info(f"{request.remote_addr} transformed from {from_string} to {to_string}")
                return format_coordinate(coordinate=result_latitude, metric=output_metric), format_coordinate(
                    coordinate=result_longitude, metric=output_metric), None
            except BaseTransformException as e:
                self.app.log.error(e.message)
                return None, None, e.message
            except Exception as e:
                self.app.log.exception(e)
                return None, None, traceback.format_exc()
