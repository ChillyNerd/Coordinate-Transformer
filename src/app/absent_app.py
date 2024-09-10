from abc import ABC, abstractmethod

from dash import Dash


class AbsentApp(ABC):

    app: Dash

    @abstractmethod
    def init_callbacks(self):
        pass

