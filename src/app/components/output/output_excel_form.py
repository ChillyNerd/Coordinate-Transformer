import dash_bootstrap_components as dbc
from dash import html, dcc, Dash

from src.app.components import BaseComponent


class OutputExcelForm(BaseComponent):
    def __init__(self, app: Dash):
        super().__init__(app)
        download_button = dbc.Button('Пересчет', id='download_excel_file', className="download-excel-file")
        download_data = dcc.Download(id='excel_download_data')
        form = html.Div(children=[download_button, download_data], className="border-top padding-top",
                        id='output_excel_form')
        self.layout = form

    def init_callbacks(self):
        pass
