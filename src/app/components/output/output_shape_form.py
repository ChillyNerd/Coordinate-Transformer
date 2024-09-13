import os.path
import dash_bootstrap_components as dbc
import shapefile
from dash import html, dcc, Output, Input, State
from dash.exceptions import PreventUpdate
from flask import request

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.coordinate_transformer import projections_dict, CoordinateTransformer


class OutputShapeForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        download_button = dbc.Button('Пересчет', id='download_shape_file', className="download-shape-file")
        download_data = dcc.Download(id='shape_download_data')
        form = html.Div(children=[download_button, download_data], className="border-top padding-top",
                        id='output_shape_form')
        self.layout = form
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback([
            Output('output_shape_form', 'className')
        ], [
            Input('shape_files', 'data'),
            Input('tabs_select', 'active_tab'),
            State('output_shape_form', 'className')
        ])
        def show_shape_form(shape_file, selected_tab, output_classes):
            classes = output_classes.split()
            if shape_file is None or selected_tab != 'shape_tab':
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]

        @self.dash_app.callback(
            Output('shape_download_data', 'data'),
            Input('download_shape_file', 'n_clicks'),
            State('zone_from_select', 'value'),
            State('zone_to_select', 'value'),
            State('shape_files', 'data'),
        )
        def download_shape_file(clicks, projection_from, projection_to, shape_files):
            if clicks:
                shape_input_directory = os.path.join(
                    self.app.config.files_path, request.remote_addr, 'shape_input'
                )
                result_directory = os.path.join(shape_input_directory, 'result')
                zip_filename = os.path.join(shape_input_directory, 'result.zip')
                for shape_file in shape_files:
                    shpf = shapefile.Reader(shape_file)
                    file_name = os.path.basename(shape_file)
                    if not os.path.exists(result_directory):
                        os.mkdir(result_directory)
                    new_shape_path = os.path.join(result_directory, f'result_{file_name}')
                    new_shape = shapefile.Writer(new_shape_path, shapefile.POLYLINE)
                    new_shape.fields = shpf.fields
                    transformator = CoordinateTransformer(
                        projection_from=projections_dict[projection_from],
                        projection_to=projections_dict[projection_to],
                    )
                    for feature in shpf.shapeRecords():
                        geom = feature.shape.points
                        new_points = []
                        for coords in geom:
                            x, y = coords[0], coords[1]
                            new_x, new_y = transformator.transform(x, y)
                            new_points.append([new_x, new_y])
                        feature.shape.points = new_points
                        new_shape.record(*feature.record)
                        new_shape.shape(feature.shape)
                    self.app.replace_shape_prj(new_shape_path, projection_to)
                self.app.zip_directory(result_directory, zip_filename)
                return dcc.send_file(zip_filename, filename='result.zip', type='application/zip')
            raise PreventUpdate
