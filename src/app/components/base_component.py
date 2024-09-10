from abc import ABC, abstractmethod

from dash import Dash


class BaseComponent(ABC):

    layout = None

    def __init__(self, app: Dash):
        self.app = app

    @abstractmethod
    def init_callbacks(self):
        pass

    def get_layout(self):
        return self.layout
