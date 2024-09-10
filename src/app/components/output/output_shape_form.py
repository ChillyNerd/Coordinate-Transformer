import dash_bootstrap_components as dbc
from dash import html, dcc, Dash

from src.app.components import BaseComponent


class OutputShapeForm(BaseComponent):
    def __init__(self, app: Dash):
        super().__init__(app)
        download_button = dbc.Button('Пересчет', id='download_shape_file', className="download-shape-file")
        download_data = dcc.Download(id='shape_download_data')
        form = html.Div(children=[download_button, download_data], className="border-top padding-top",
                        id='output_shape_form')
        self.layout = form

    def init_callbacks(self):
        pass
