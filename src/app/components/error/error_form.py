import dash_bootstrap_components as dbc
from dash import Dash

from src.app.components import BaseComponent


class ErrorForm(BaseComponent):
    def __init__(self, app: Dash):
        super().__init__(app)
        form = dbc.Alert(dismissable=True, color='warning', is_open=False, id='error', duration=4000,
                         className="error-form")
        self.layout = form

    def init_callbacks(self):
        pass
