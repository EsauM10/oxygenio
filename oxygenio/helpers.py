from typing import Literal
from flask import Flask, render_template

BrowserType = Literal['chrome']
ModeType = Literal['dev', 'build']

def _root():
    return render_template('index.html')

def create_app(app_name: str, template_folder: str, static_folder: str) -> Flask:
    app = Flask(app_name, template_folder=template_folder, static_folder=static_folder)
    app.add_url_rule('/', view_func=_root)
    return app

def create_file(filename: str, data: str):
    with open(filename, mode='w') as file:
        file.write(data)

def read_file(filename: str) -> str:
    with open(filename, mode='r') as file:
        return file.read()