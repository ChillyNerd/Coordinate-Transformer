import dash_bootstrap_components as dbc
from dash import html, dcc, Dash, Output, Input, State

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent


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
