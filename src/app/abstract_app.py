from abc import ABC, abstractmethod
from logging import Logger

from dash import Dash


class AbstractApp(ABC):
    app: Dash
    log: Logger

    @abstractmethod
    def init_callbacks(self):
        pass

    @abstractmethod
    def upload_file(self, client_address, file_type: str, file: dict):
        pass

    @staticmethod
    @abstractmethod
    def save_file(directory_path, filename, content):
        pass

    @abstractmethod
    def refresh_or_create_directory(self, client_address, file_type: str):
        pass

    @abstractmethod
    def delete_clients_repo(self, client_address):
        pass

    @abstractmethod
    def delete_files(self, client_address, file_type):
        pass

    @abstractmethod
    def recursive_files_delete(self, filepath):
        pass
