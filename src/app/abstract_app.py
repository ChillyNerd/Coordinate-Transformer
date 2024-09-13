from abc import ABC, abstractmethod
from logging import Logger

from dash import Dash

from src.config import Config


class AbstractApp(ABC):
    app: Dash
    config: Config
    log: Logger

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

    @abstractmethod
    def replace_shape_prj(self, shape_file, projection_from):
        pass

    @staticmethod
    @abstractmethod
    def zip_directory(directory_path, filename):
        pass
