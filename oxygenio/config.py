import json
import os

from oxygenio.helpers import CONFIG_FILENAME, ROOT_PATH, ModeType, read_file

paths = [
    os.path.join(os.getcwd(), CONFIG_FILENAME),
    os.path.join(ROOT_PATH, CONFIG_FILENAME)
]

class ConfigLoader:
    def __init__(self) -> None:
        self.__mode: ModeType = 'dev'
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
        for path in paths:
            if(os.path.exists(path)):
                self.file = path
                break
        else:
            raise FileNotFoundError(f'Oxygen {CONFIG_FILENAME} not found. Run: oxygen create')
        
        data = json.loads(read_file(self.file))

        self.__mode = 'build' if(data['mode'] == 'build') else 'dev'
        self.app_url = str(data['appURL'])
        self.dev_command = str(data['devCommand'])
        self.build_command = str(data['buildCommand'])
        self.dist_folder = str(data['distFolder'])
        self.frontend_app = str(data['frontendApp'])