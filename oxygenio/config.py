import json

from oxygenio.helpers import ModeType


class ConfigLoader:
    def __init__(self, config_file: str) -> None:
        self.mode: ModeType = 'dev'
        self.dev_command = ''
        self.build_command = ''
        self.app_url = ''
        self.dist_folder = ''
        self.load(config_file)
    
    def load(self, config_file: str):
        with open(config_file, mode='r') as file:
            data = json.loads(file.read())

        mode = str(data['mode'])
        if(mode != 'dev' and mode != 'build'):
            raise Exception(f'Expecting one of: {["dev", "build"]}')

        self.mode = mode
        self.dev_command = str(data['devCommand'])
        self.build_command = str(data['buildCommand'])
        self.app_url = str(data['appURL'])
        self.dist_folder = str(data['distFolder'])