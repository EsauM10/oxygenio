import os
from typing import Any, Callable

from flask_socketio import SocketIO

from oxygenio.browsers import Chrome
from oxygenio.config import ConfigLoader
from oxygenio.helpers import BrowserType, create_app


class Oxygenio:
    def __init__(self, config_file: str = 'config.json') -> None:
        self.config = ConfigLoader(config_file)
        self.__socketio = SocketIO()
    
    def on(self, func: Callable[..., Any]):
       self.__socketio.on_event(func.__name__, func)
    
    def _get_app_url(self, host: str, port: int) -> str:
        if(self.config.mode == 'dev'):
            return self.config.app_url
        return f'http://{host}:{port}'

    def _get_assets_folders(self) -> tuple[str, str]:
        if(self.config.mode == 'dev'):
            return 'templates', 'static'
        
        work_dir = os.getcwd()
        template_folder = os.path.join(work_dir, self.config.dist_folder)
        static_folder = os.path.join(template_folder, 'assets')
        return template_folder, static_folder

    def run(self, host: str = 'localhost', port: int = 8000, browser: BrowserType = 'chrome'):
        debug = self.config.mode == 'dev'

        if(browser == 'chrome'):
            Chrome().run(url=self._get_app_url(host, port))

        app = create_app(__name__, *self._get_assets_folders())
        self.__socketio.init_app(app)
        self.__socketio.run(app, host=host, port=port, debug=debug, use_reloader=False, log_output=False)