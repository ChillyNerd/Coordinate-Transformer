import dash_bootstrap_components as dbc
from dash import html

from src.app.components.input.input_excel_form import form as input_excel_form
from src.app.components.input.input_manual_form import form as input_manual_form

tabs = dbc.Tabs(
    [
        dbc.Tab(
            input_manual_form,
            label='Ручной ввод',
            label_class_name='display-4',
            tab_id='manual_tab'
        ),
        dbc.Tab(
            input_excel_form,
            label='Excel',
            label_class_name='display-4',
            tab_id='excel_tab'
        ),
        dbc.Tab(
            label='Shape',
            label_class_name='display-4',
            tab_id='shape_tab'
        )
    ],
    active_tab='manual_tab',
    id='tabs_select'
)
input_tab_form = html.Div(children=[tabs], className="column-gap", id="input_tabs")
