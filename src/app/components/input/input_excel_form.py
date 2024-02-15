import dash_bootstrap_components as dbc
from dash import dcc, html

upload_button = dcc.Upload(dbc.Button('Загрузить файл'), id='upload_excel_file', className="upload-excel-file")
delete_button = dbc.Button('╳', id='delete_excel_file', color='danger', className='delete-excel-file align-center')
buttons = html.Div(children=[upload_button, delete_button], className='row-gap')
excel_file_name = html.Div('Выберите файл', id='excel_file_name', className="file-name")
form = html.Div(children=[buttons, excel_file_name], className="upload-excel-form row-gap long-gap")
