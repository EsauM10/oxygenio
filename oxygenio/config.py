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
        self.__frontend_app = ''
        self.__dist_folder = ''
        self.static_folder = ''
        self.__load()
    
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
    
    def __load(self):
        for path in paths:
            if(os.path.exists(path)):
                self.file = path
                break
        else:
            raise FileNotFoundError(f'Config file {CONFIG_FILENAME} not found, run: oxygen init')
        
        data = json.loads(read_file(self.file))

        self.__mode = 'build' if(data['mode'] == 'build') else 'dev'
        self.app_url = str(data['appURL'])
        self.dev_command = str(data['devCommand'])
        self.build_command = str(data['buildCommand'])
        self.__frontend_app = str(data['frontendApp'])
        self.__dist_folder = str(data['distFolder'])
        self.static_folder = str(data['staticFolder'])
