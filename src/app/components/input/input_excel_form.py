import dash_bootstrap_components as dbc
from src.app.assets.icons import delete_icon, inspect_icon
from dash import dcc, html

upload_button = dcc.Upload(dbc.Button('Загрузить файл'), id='upload_excel_file', className="upload-file")
delete_button = dbc.Button(
    html.Img(src=delete_icon, className='common-icon'),
    id='delete_excel_file', color='danger', className='action-button align-center'
)
inspect_button = dbc.Button(
    html.Img(src=inspect_icon, className='common-icon'),
    id='inspect_excel_file', color='secondary', className='action-button align-center'
)
buttons = html.Div(children=[upload_button, delete_button, inspect_button], className='row-gap')
excel_file_name = html.Div('Выберите файл', id='excel_file_name', className="file-name")
form = html.Div(children=[buttons, excel_file_name], className="upload-form row-gap long-gap")
