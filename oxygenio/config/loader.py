import json
import os
from typing import Any

from oxygenio.config.build import BuildConfig
from oxygenio.config.window import WindowConfig
from oxygenio.helpers import (
    CONFIG_FILENAME, 
    ROOT_PATH,
    read_file
)

paths = [
    os.path.join(os.getcwd(), CONFIG_FILENAME),
    os.path.join(ROOT_PATH, CONFIG_FILENAME)
]

class ConfigLoader:
    def __init__(self) -> None:
        data = self.__parse_config()

        self.config_file = CONFIG_FILENAME
        self.build = BuildConfig.from_dict(data)
        self.window = WindowConfig.from_dict(data)
    
    @property
    def app_url(self) -> str:
        return self.build.app_url
    
    @property
    def build_command(self) -> str:
        return self.build.build_command

    @property
    def dist_path(self) -> str:
        return os.path.join(self.frontend_app_path, self.build.dist_folder)
    
    @property
    def frontend_app_path(self) -> str:
        return os.path.join(os.getcwd(), self.build.app)
    
    @property
    def is_dev_mode(self) -> bool:
        return self.build.mode == 'dev'
    
    @property
    def is_windowed(self) -> bool:
        return self.window.console == False

    @property
    def static_folder(self) -> str:
        return self.build.static_folder

    @property
    def to_dict(self) -> dict[str, str]:
        return self.build.to_dict
    
    @property
    def labels(self) -> dict[str, str]:
        return {
            'OXYGEN_MAXIMIZE': str(self.window.maximize).lower(),
            'OXYGEN_RESIZABLE': str(self.window.resizable).lower(),
            'OXYGEN_WIDTH': str(self.window.width),
            'OXYGEN_HEIGHT': str(self.window.height)
        }

    def __parse_config(self) -> dict[str, Any]:
        for path in paths:
            if(os.path.exists(path)):
                self.config_file = path
                break
        else:
            raise FileNotFoundError(f'Config file {CONFIG_FILENAME} not found, run: oxygen init')
        
        return json.loads(read_file(self.config_file))

