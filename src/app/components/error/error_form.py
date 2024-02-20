import dash_bootstrap_components as dbc

form = dbc.Alert(dismissable=True, color='warning', is_open=False, id='error', duration=4000, className="error-form")
