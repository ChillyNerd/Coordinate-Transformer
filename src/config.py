import os
import socket

import yaml


class Config:
    __host = socket.gethostname()
    __port = 7070
    src_path = os.path.join(os.getcwd(), 'src')
    map_path = os.path.join(src_path, 'app', 'map')
    files_path = os.path.join(src_path, 'app', 'files')

    def __init__(self, config_path: str = None):
        if config_path is None or not os.path.exists(config_path):
            self.path = None
            return
        if not os.path.exists(self.files_path):
            os.mkdir(self.files_path)
        self.path = config_path
        with open(self.path, encoding='utf-8') as file:
            config_file = yaml.load(file, Loader=yaml.FullLoader)
            self.set_config_parameter('host', config_file, str, 'app', 'host')
            self.set_config_parameter('port', config_file, str, 'app', 'port')

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
