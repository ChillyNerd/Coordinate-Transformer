from dash import dcc, html
import dash_bootstrap_components as dbc

upload_button = dcc.Upload(dbc.Button('Загрузить файл'), id='upload_excel_file')
form = html.Div(children=[upload_button], className="input-form")
