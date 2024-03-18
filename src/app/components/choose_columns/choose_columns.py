from dash import html
import dash_bootstrap_components as dbc


latitude_column_label = html.Div("Колонка широты", className='label-form')
latitude_column_input = dbc.Select(id='latitude_column_select')
latitude_column_form = html.Div(children=[latitude_column_label, latitude_column_input], className="row-between")

longitude_column_label = html.Div("Колонка долготы", className='label-form')
longitude_column_input = dbc.Select(id='longitude_column_select')
longitude_column_form = html.Div(children=[longitude_column_label, longitude_column_input], className="row-between")

choose_column_dialog_body = html.Div([latitude_column_form, longitude_column_form], className='column-gap')

choose_column_dialog = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Выбор колонок")),
        dbc.ModalBody(choose_column_dialog_body),
        dbc.ModalFooter(
            [
                dbc.Button(
                    "Подтвердить выбор", id="confirm_columns", n_clicks=0
                )
            ]
        )
    ],
    id="choose_column_dialog",
    backdrop='static',
    centered=True,
    is_open=False,
)
