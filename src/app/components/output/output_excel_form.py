import os

import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, State
from dash.exceptions import PreventUpdate

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.coordinate_transformer import projections_dict
from src.excel_transformer import ExcelTransformer


class OutputExcelForm(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        download_button = dbc.Button('Пересчет', id='download_excel_file', className="download-excel-file")
        download_data = dcc.Download(id='excel_download_data')
        form = html.Div(children=[download_button, download_data], className="border-top padding-top",
                        id='output_excel_form')
        self.layout = form
        self.init_callbacks()

    def init_callbacks(self):
        @self.dash_app.callback(
            Output('excel_download_data', 'data'),
            Input('download_excel_file', 'n_clicks'),
            State('zone_from_select', 'value'),
            State('zone_to_select', 'value'),
            State('latitude_column_select', 'value'),
            State('longitude_column_select', 'value'),
            State('upload_excel_file', 'filename'),
            State('excel_file', 'data'),
            State('metrics_select', 'value'),
        )
        def download_excel_file(clicks, projection_from, projection_to, latitude_column, longitude_column, file_name,
                                excel_file, metric):
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

        @self.dash_app.callback([
            Output('output_excel_form', 'className')
        ], [
            Input('points', 'data'),
            Input('tabs_select', 'active_tab'),
            State('output_excel_form', 'className')
        ])
        def show_excel_form(points, selected_tab, output_classes):
            classes = output_classes.split()
            if points is None or len(points) == 0 or selected_tab != 'excel_tab':
                if self.hidden not in classes:
                    classes.append(self.hidden)
            else:
                if self.hidden in classes:
                    classes = list(filter(lambda class_name: class_name != self.hidden, classes))
            return [' '.join(classes)]
