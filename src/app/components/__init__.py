from dash import html, dcc

from src.app.abstract_app import AbstractApp
from src.app.components.base_component import BaseComponent
from src.app.components.choose_columns.choose_columns import ChooseColumns
from src.app.components.error.error_form import ErrorForm
from src.app.components.split.split import SplitPane


class Layout:

    def __init__(self, app: AbstractApp):
        self.app = app

    def get_layout(self):
        layout = html.Div(
            children=[
                dcc.Store(id='latitude'),
                dcc.Store(id='longitude'),
                dcc.Store(id='numeric_latitude'),
                dcc.Store(id='numeric_longitude'),
                dcc.Store(id='angle_latitude'),
                dcc.Store(id='angle_longitude'),
                dcc.Store(id='excel_file'),
                dcc.Store(id='shape_archive'),
                dcc.Store(id='excel_columns'),
                dcc.Store(id='toggle_choose_column_dialog'),
                dcc.Store(id='points'),
                dcc.Store(id='manual_points'),
                dcc.Store(id='excel_points'),
                dcc.Store(id='shape_files'),
                dcc.Store(id='transform_error'),
                dcc.Store(id='excel_upload_error'),
                dcc.Store(id='shape_upload_error'),
                dcc.Store(id='excel_read_error'),
                dcc.Store(id='shape_read_error'),
                dcc.Store(id='excel_show_error'),
                SplitPane(self.app).get_layout(),
                ChooseColumns(self.app).get_layout(),
                ErrorForm(self.app).get_layout()
            ],
            className="column-gap"
        )
        return layout
