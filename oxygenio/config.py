import json
import os
from pathlib import Path

from oxygenio.helpers import ModeType, read_file

ROOT_PATH = str(Path(__file__).parent.parent)

class ConfigLoader:
    def __init__(self, build: bool = False) -> None:
        self.__mode: ModeType = 'build' if(build) else 'dev'
        self.file = 'config.json'
        self.dev_command = ''
        self.build_command = ''
        self.app_url = ''
        self.dist_folder = ''
        self.load()
    
    @property
    def is_dev_mode(self) -> bool:
        return self.__mode == 'dev'

    def load(self):
        if(not self.is_dev_mode):
            self.file = os.path.join(ROOT_PATH, 'config.json')
        
        data = json.loads(read_file(self.file))

        self.dev_command = str(data['devCommand'])
        self.build_command = str(data['buildCommand'])
        self.app_url = str(data['appURL'])
        self.dist_folder = str(data['distFolder'])