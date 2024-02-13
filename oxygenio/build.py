import json
import os
import shutil
import tempfile

from oxygenio.config import ConfigLoader
from oxygenio.helpers import (
    CONFIG_FILENAME,
    create_file, run_command
)

class ViteBuilder:
    def __init__(self, config: ConfigLoader) -> None:
        self.config = config

    def create_config_file(self, filename: str):
        data = self.config.to_dict
        data['mode'] = 'build'
        create_file(filename, json.dumps(data, indent=4))

    def create_templates_folder(self, templates_path: str):
        os.mkdir(templates_path)
        for filename in os.listdir(self.config.dist_path):
            file = os.path.join(self.config.dist_path, filename)
            if(os.path.isfile(file)):
                destination = os.path.join(templates_path, filename)
                shutil.copyfile(file, destination)

    def build(self):
        run_command(self.config.build_command.split(' '))
        tempdir = tempfile.TemporaryDirectory()
        
        try:
            assets_folder = os.path.join(self.config.dist_path, 'assets')
            config_file = os.path.join(tempdir.name, CONFIG_FILENAME)
            static_temp_folder = os.path.join(tempdir.name, 'static')
            templates_temp_folder = os.path.join(tempdir.name, 'templates')
            
            shutil.copytree(src=assets_folder, dst=static_temp_folder)
            self.create_templates_folder(templates_temp_folder)
            self.create_config_file(config_file)

            run_command([
                'pyinstaller', '--noconfirm', '--onefile', '--windowed', '--clean',
                f'--add-data={config_file}:.',
                f'--add-data={static_temp_folder}:{self.config.static_folder}',
                f'--add-data={templates_temp_folder}:templates',
                '--hidden-import=engineio.async_drivers.gevent',
                'main.py'
            ])
        except Exception as ex:
            raise ex
        finally:
            print(f'Cleanup directory: {tempdir.name} 🧹')
            tempdir.cleanup()
            os.remove('main.spec')