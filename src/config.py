import datetime
import logging
import logging.handlers
import os
import socket

import yaml


class Config:
    __host = socket.gethostname()
    __port = 7070
    __logging_level: str = logging.INFO
    src_path = os.path.join(os.getcwd(), 'src')
    map_path = os.path.join(src_path, 'app', 'map')
    files_path = os.path.join(src_path, 'app', 'files')
    coordinate_transformer = 'CoordinateTransformer'
    application_server = 'ApplicationServer'
    main = 'Main'

    def __init__(self, config_path: str = None):
        if config_path is not None and os.path.exists(config_path):
            with open(config_path, encoding='utf-8') as file:
                config_file = yaml.load(file, Loader=yaml.FullLoader)
                self.set_config_parameter('host', config_file, str, 'app', 'host')
                self.set_config_parameter('port', config_file, str, 'app', 'port')
                self.set_config_parameter('logging_level', config_file, str, 'log', 'level')
                self.set_config_parameter('application_server', config_file, str, 'log', 'name', 'app')
                self.set_config_parameter('coordinate_transformer', config_file, str, 'log', 'name', 'transformer')
                self.set_config_parameter('main', config_file, str, 'log', 'name', 'main')
        if not os.path.exists(self.files_path):
            os.mkdir(self.files_path)
        self.config_logging()

    def config_logging(self):
        current_date = str(datetime.datetime.now().date())
        logs_path = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
        handler = logging.handlers.RotatingFileHandler(os.path.join(logs_path, f'{current_date}.log'), mode='a',
                                                       maxBytes=5_000_000, backupCount=1000)
        logger_handlers = [handler, logging.StreamHandler()]
        logging.basicConfig(format='%(asctime)s - %(name)21s %(levelname)-7s %(threadName)12s: %(message)s',
                            handlers=logger_handlers, level=logging.getLevelName(self.logging_level))
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

    def set_config_parameter(self, config_parameter, config_file: dict, parameter_type: type, *parameter_names):
        if len(parameter_names) == 0:
            return
        inner_config = config_file
        for parameter_name in parameter_names:
            if not isinstance(inner_config, dict) or parameter_name not in inner_config.keys():
                return
            inner_config = inner_config[parameter_name]
        if not isinstance(inner_config, dict):
            self.__setattr__(config_parameter, parameter_type(inner_config))

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, value: str):
        self.__host = value

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, value: int):
        self.__port = value

    @property
    def logging_level(self) -> str:
        return self.__logging_level

    @logging_level.setter
    def logging_level(self, value: str):
        self.__logging_level = value
