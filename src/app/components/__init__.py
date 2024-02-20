from dash import html, dcc
from src.app.components.split.split import split_pane
from src.app.components.error.error_form import form as error

layout = html.Div(
    children=[
        dcc.Store(id='latitude'),
        dcc.Store(id='longitude'),
        dcc.Store(id='numeric_latitude'),
        dcc.Store(id='numeric_longitude'),
        dcc.Store(id='angle_latitude'),
        dcc.Store(id='angle_longitude'),
        dcc.Store(id='excel_file'),
        dcc.Store(id='points'),
        dcc.Store(id='manual_points'),
        dcc.Store(id='excel_points'),
        dcc.Store(id='transform_error'),
        dcc.Store(id='excel_upload_error'),
        dcc.Store(id='excel_read_error'),
        split_pane,
        error
    ],
    className="column-gap"
)
