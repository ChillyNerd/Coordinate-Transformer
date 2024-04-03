import dash_bootstrap_components as dbc
from src.app.assets.icons import delete_icon
from dash import dcc, html

upload_button = dcc.Upload(dbc.Button('Загрузить файл'), id='upload_shape_file', className="upload-file")
delete_button = dbc.Button(
    html.Img(src=delete_icon, className='common-icon'),
    id='delete_shape_file', color='danger', className='action-button align-center'
)
buttons = html.Div(children=[upload_button, delete_button], className='row-gap')
excel_file_name = html.Div('Выберите файл', id='shape_file_name', className="file-name")
form = html.Div(children=[buttons, excel_file_name], className="upload-form row-gap long-gap")
