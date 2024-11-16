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

def install_node_dependencies(config: ConfigLoader):
    os.chdir(config.frontend_app_path)
    run_command(['npm', 'i'])
    os.chdir('..')

class ViteBuilder:
    def __init__(self, config: ConfigLoader) -> None:
        self.config = config

    def create_config_file(self, filename: str):
        data = self.config.to_dict
        data['mode'] = 'build'
        create_file(filename, json.dumps(data, indent=4))

    def create_static_folder(self, static_path: str):
        vite_assets_folder = os.path.join(self.config.dist_path, 'assets')
        shutil.copytree(src=vite_assets_folder, dst=static_path)     

    def get_pyinstaller_flags(self) -> list[str]:
        flags = ['--noconfirm', '--onefile', '--clean']

        if(self.config.is_windowed):
            flags.append('--windowed')
        return flags

    def get_public_files(self) -> list[str]:
        files = []

        for name in os.listdir(self.config.dist_path):
            if(name in ['assets', INDEX_HTML]):
                continue

            source = os.path.join(self.config.dist_path, name)
            destination = '.' if(os.path.isfile(source)) else name
            files.append(f'--add-data={source}:{destination}')
        return files

    def create_templates_folder(self, templates_path: str):
        os.mkdir(templates_path)
        index_html = os.path.join(self.config.dist_path, INDEX_HTML)
        destination = os.path.join(templates_path, INDEX_HTML)
        shutil.copyfile(index_html, destination)

    def create_oxygen_js(self, ):
        oxygen_js = os.path.join(DATA_DIR, 'oxygen.js')
        destination = os.path.join(self.config.dist_path, 'assets', 'oxygen.js')
        shutil.copyfile(oxygen_js, destination)

    def create_favicon(self):
        vite_favicon = os.path.join(self.config.dist_path, FAVICON)
        
        if(not os.path.exists(vite_favicon)):
            oxygen_favicon = os.path.join(DATA_DIR, FAVICON)
            shutil.copyfile(oxygen_favicon, vite_favicon)
    
    def add_tags_to_html(self, html_path: str):
        soup = BeautifulSoup(read_file(html_path), 'html.parser')
        head_tag = soup.find('head')
        link_tag = soup.new_tag('link', rel='shortcut icon', href=f'{FAVICON}')
        script_tag = soup.new_tag('script', type='module', crossorigin=None, src='/assets/oxygen.js')

        title = self.config.window.title
        head_tag.find('title').string.replace_with(title) # type: ignore
        head_tag.append(script_tag) # type: ignore
        head_tag.append(link_tag) #type: ignore
        create_file(html_path, soup.prettify())

    def node_modules_exists(self) -> bool:
        node_modules_path = os.path.join(self.config.frontend_app_path, 'node_modules')
        return os.path.exists(node_modules_path)

    def build(self):
        if(not self.node_modules_exists()):
            install_node_dependencies(self.config)

        run_command(self.config.build_command.split(' '))
        tempdir = tempfile.TemporaryDirectory()
        
        try:
            config_file = os.path.join(tempdir.name, CONFIG_FILENAME)
            favicon_path = os.path.join(self.config.dist_path, FAVICON)
            static_temp_folder = os.path.join(tempdir.name, 'static')
            templates_temp_folder = os.path.join(tempdir.name, 'templates')
            index_html_path = os.path.join(templates_temp_folder, INDEX_HTML)

            self.create_oxygen_js()
            self.create_static_folder(static_temp_folder)
            self.create_templates_folder(templates_temp_folder)
            self.create_config_file(config_file)
            self.create_favicon()
            self.add_tags_to_html(index_html_path)

            run_command([
                'pyinstaller',
                *self.get_pyinstaller_flags(),
                *self.get_public_files(),
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