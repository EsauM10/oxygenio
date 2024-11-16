import json
import os
from typing import Any

from oxygenio.config.window import WindowConfig
from oxygenio.helpers import (
    CONFIG_FILENAME, 
    ROOT_PATH, 
    ModeType, 
    read_file
)

paths = [
    os.path.join(os.getcwd(), CONFIG_FILENAME),
    os.path.join(ROOT_PATH, CONFIG_FILENAME)
]

class ConfigLoader:
    def __init__(self) -> None:
        data = self.__parse_config()

        self.__mode: ModeType = 'dev'
        self.config_file = CONFIG_FILENAME
        self.dev_command = ''
        self.build_command = ''
        self.app_url = ''
        self.__frontend_app = ''
        self.__dist_folder = ''
        self.static_folder = ''

        self.__load_build_data(data)
        self.window = WindowConfig.from_dict(data)
    
    @property
    def dist_path(self) -> str:
        return os.path.join(self.frontend_app_path, self.__dist_folder)
    
    @property
    def frontend_app_path(self) -> str:
        return os.path.join(os.getcwd(), self.__frontend_app)
    
    @property
    def is_dev_mode(self) -> bool:
        return self.__mode == 'dev'
    
    @property
    def to_dict(self) -> dict[str, str]:
        return {
            'mode': self.__mode,
            'appURL': self.app_url,
            'devCommand': self.dev_command,
            'buildCommand': self.build_command,
            'frontendApp': self.__frontend_app,
            'distFolder': self.__dist_folder,
            'staticFolder': self.static_folder
        }
    
    def __parse_config(self) -> dict[str, Any]:
        for path in paths:
            if(os.path.exists(path)):
                self.config_file = path
                break
        else:
            raise FileNotFoundError(f'Config file {CONFIG_FILENAME} not found, run: oxygen init')
        
        return json.loads(read_file(self.config_file))

    def __load_build_data(self, data: dict[str, Any]):
        self.__mode = 'build' if(data['mode'] == 'build') else 'dev'
        self.app_url = str(data['appURL'])
        self.dev_command = str(data['devCommand'])
        self.build_command = str(data['buildCommand'])
        self.__frontend_app = str(data['frontendApp'])
        self.__dist_folder = str(data['distFolder'])
        self.static_folder = str(data['staticFolder'])
