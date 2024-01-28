import json
import os
from pathlib import Path

from oxygenio.helpers import ModeType, read_file

ROOT_PATH = str(Path(__file__).parent.parent)
CONFIG_FILENAME = 'config.json'


class ConfigLoader:
    def __init__(self, build: bool = False) -> None:
        self.__mode: ModeType = 'build' if(build) else 'dev'
        self.file = CONFIG_FILENAME
        self.dev_command = ''
        self.build_command = ''
        self.app_url = ''
        self.dist_folder = ''
        self.frontend_app = ''
        self.__load()
    
    @property
    def dist_path(self) -> str:
        return os.path.join(self.frontend_app, self.dist_folder)
    
    @property
    def is_dev_mode(self) -> bool:
        return self.__mode == 'dev'
    
    def __load(self):
        if(not self.is_dev_mode):
            self.file = os.path.join(ROOT_PATH, CONFIG_FILENAME)
        
        data = json.loads(read_file(self.file))

        self.app_url = str(data['appURL'])
        self.dev_command = str(data['devCommand'])
        self.build_command = str(data['buildCommand'])
        self.dist_folder = str(data['distFolder'])
        self.frontend_app = str(data['frontendApp'])