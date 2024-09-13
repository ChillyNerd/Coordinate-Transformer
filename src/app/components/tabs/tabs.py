import dash_bootstrap_components as dbc
from dash import html

from src.app.abstract_app import AbstractApp
from src.app.components import BaseComponent
from src.app.components.input.input_excel_form import InputExcelForm
from src.app.components.input.input_manual_form import InputManualForm
from src.app.components.input.input_shape_form import InputShapeForm


class Tabs(BaseComponent):
    def __init__(self, app: AbstractApp):
        super().__init__(app)
        tabs = dbc.Tabs(
            [
                dbc.Tab(
                    InputManualForm(self.app).get_layout(),
                    label='Ручной ввод',
                    label_class_name='display-4',
                    tab_id='manual_tab'
                ),
                dbc.Tab(
                    InputExcelForm(self.app).get_layout(),
                    label='Excel',
                    label_class_name='display-4',
                    tab_id='excel_tab'
                ),
                dbc.Tab(
                    InputShapeForm(self.app).get_layout(),
                    label='Shape',
                    label_class_name='display-4',
                    tab_id='shape_tab'
                )
            ],
            active_tab='manual_tab',
            id='tabs_select'
        )
        input_tab_form = html.Div(children=[tabs], className="column-gap", id="input_tabs")
        self.layout = input_tab_form
        self.init_callbacks()

    def init_callbacks(self):
        pass
