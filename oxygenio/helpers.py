import os
from pathlib import Path
import subprocess
from typing import Literal
from flask import Flask, render_template

ModeType = Literal['dev', 'build']

CONFIG_FILENAME = 'oxygen.json'
FAVICON  = 'favicon.ico'
INDEX_HTML = 'index.html' 
BASEDIR  = str(Path(__file__).parent)
DATA_DIR = os.path.join(BASEDIR, 'data')
ROOT_PATH = str(Path(__file__).parent.parent)


def _root():
    return render_template(INDEX_HTML)

def create_app(app_name: str, template_folder: str = 'templates', static_folder: str = 'static') -> Flask:
    app = Flask(app_name, template_folder=template_folder, static_folder=static_folder)
    app.add_url_rule('/', view_func=_root)
    return app

def create_file(filename: str, data: str):
    with open(filename, mode='w') as file:
        file.write(data)

def read_file(filename: str) -> str:
    with open(filename, mode='r') as file:
        return file.read()

def run_command(commands: list[str]):
    subprocess.call(commands, shell=True)