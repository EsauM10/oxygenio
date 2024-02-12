import json
import os
import shutil
import tempfile

from bs4 import BeautifulSoup

from oxygenio.config import ConfigLoader
from oxygenio.helpers import (
    CONFIG_FILENAME,
    read_file, create_file, run_command
)

class ViteBuilder:
    def __init__(self, config: ConfigLoader) -> None:
        self.config = config

    def create_config_file(self, filename: str):
        data = self.config.to_dict
        data['mode'] = 'build'
        create_file(filename, json.dumps(data, indent=4))

    def create_index_file(self, filename: str, assets_folder: str):
        index_file = os.path.join(self.config.dist_path, 'index.html')
        html_content = self.update_index_file(index_file, assets_folder)
        create_file(filename, html_content)

    def update_index_file(self, filename: str, assets_folder: str) -> str:
        assets_filenames = os.listdir(assets_folder)
        javascript_file = list(filter(lambda file: file.endswith('.js'), assets_filenames))[0]
        css_file = list(filter(lambda file: file.endswith('.css'), assets_filenames))[0]

        if(not javascript_file.endswith('.js')):
            javascript_file = assets_filenames[1]
            css_file = assets_filenames[0]
        
        parser = BeautifulSoup(read_file(filename), 'html.parser')
        script_tag = parser.find('script', src=f'/assets/{javascript_file}')
        link_tag = parser.find('link', href=f'/assets/{css_file}')
        script_tag['src'] = "{{ " + f"url_for('static', filename='{javascript_file}')" + " }}" # type: ignore
        link_tag['href'] = "{{ " + f"url_for('static', filename='{css_file}')" + " }}" # type: ignore
        return parser.prettify()

    def build(self):
        run_command(self.config.build_command.split(' '))
        tempdir = tempfile.TemporaryDirectory()
        
        try:
            assets_folder = os.path.join(self.config.dist_path, 'assets')
            config_file = os.path.join(tempdir.name, CONFIG_FILENAME)
            static_folder = os.path.join(tempdir.name, 'static')
            templates_folder = os.path.join(tempdir.name, 'templates')
            html_file = os.path.join(templates_folder, 'index.html')
            
            os.mkdir(templates_folder)
            shutil.copytree(src=assets_folder, dst=static_folder)
            
            self.create_index_file(html_file, assets_folder)
            self.create_config_file(config_file)

            run_command([
                'pyinstaller', '--noconfirm', '--onefile', '--windowed', '--clean',
                f'--add-data={config_file}:.',
                f'--add-data={static_folder}:static',
                f'--add-data={templates_folder}:templates',
                '--hidden-import=engineio.async_drivers.gevent',
                'main.py'
            ])
        except Exception as ex:
            raise ex
        finally:
            print('Cleanup directory: 🧹', tempdir.name)
            tempdir.cleanup()
            os.remove('main.spec')