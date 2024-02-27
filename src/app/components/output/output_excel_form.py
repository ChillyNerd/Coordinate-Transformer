import dash_bootstrap_components as dbc
from dash import html, dcc

download_button = dbc.Button('Пересчет', id='download_excel_file', className="download-excel-file")
download_data = dcc.Download(id='download_data')
form = html.Div(children=[download_button, download_data], className="border-top padding-top", id='output_manual_form')
