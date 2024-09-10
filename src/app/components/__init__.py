from dash import html, dcc

from src.app.absent_app import AbsentApp
from src.app.components.base_component import BaseComponent
from src.app.components.split.split import SplitPane
from src.app.components.choose_columns.choose_columns import ChooseColumns
from src.app.components.error.error_form import ErrorForm


class Layout:

    def __init__(self, app: AbsentApp):
        self.dash_app = app.app

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
                SplitPane(self.dash_app).get_layout(),
                ChooseColumns(self.dash_app).get_layout(),
                ErrorForm(self.dash_app).get_layout()
            ],
            className="column-gap"
        )
        return layout
