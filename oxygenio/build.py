import json
import os
import shutil
import tempfile

from bs4 import BeautifulSoup

from oxygenio.config import ConfigLoader
from oxygenio.helpers import (
    CONFIG_FILENAME,
    DATA_DIR,
    FAVICON,
    INDEX_HTML,
    create_file,
    read_file, 
    run_command
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

    def create_favicon(self, favicon_path: str):
        vite_favicon = os.path.join(self.config.dist_path, FAVICON)
        
        if(os.path.exists(vite_favicon)):
            shutil.copyfile(vite_favicon, favicon_path)
        else:
            oxygen_favicon = os.path.join(DATA_DIR, FAVICON)
            shutil.copyfile(oxygen_favicon, favicon_path)
    
    def add_favicon_to_html(self, html_path: str):
        soup = BeautifulSoup(read_file(html_path), 'html.parser')
        head_tag = soup.find('head')
        href = ['{{', f'url_for("static", filename="{FAVICON}")', '}}']
        link_tag = soup.new_tag('link', rel='shortcut icon', href=' '.join(href))
        head_tag.append(link_tag) #type: ignore
        create_file(html_path, soup.prettify())

    def build(self):
        run_command(self.config.build_command.split(' '))
        tempdir = tempfile.TemporaryDirectory()
        
        try:
            assets_folder = os.path.join(self.config.dist_path, self.config.static_folder)
            config_file = os.path.join(tempdir.name, CONFIG_FILENAME)
            static_temp_folder = os.path.join(tempdir.name, 'static')
            templates_temp_folder = os.path.join(tempdir.name, 'templates')
            favicon_path = os.path.join(static_temp_folder, FAVICON)
            index_html_path = os.path.join(templates_temp_folder, INDEX_HTML)

            shutil.copytree(src=assets_folder, dst=static_temp_folder)
            self.create_templates_folder(templates_temp_folder)
            self.create_config_file(config_file)
            self.create_favicon(favicon_path)
            self.add_favicon_to_html(index_html_path)

            run_command([
                'pyinstaller', '--noconfirm', '--onefile', '--windowed', '--clean',
                f'--add-data={config_file}:.',
                f'--add-data={static_temp_folder}:{self.config.static_folder}',
                f'--add-data={templates_temp_folder}:templates',
                f'--icon={favicon_path}',
                '--hidden-import=engineio.async_drivers.gevent',
                'main.py'
            ])
        except Exception as ex:
            raise ex
        finally:
            print(f'Cleanup directory: {tempdir.name} 🧹')
            tempdir.cleanup()
            os.remove('main.spec')