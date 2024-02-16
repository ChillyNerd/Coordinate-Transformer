import dash_bootstrap_components as dbc
from dash import html

download_button = dbc.Button('Пересчет', id='download_excel_file', className="download-excel-file")
form = html.Div(children=[download_button], className="border-top padding-top", id='output_manual_form')
