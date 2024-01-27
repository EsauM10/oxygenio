import os
from typing import Any, Callable

from flask_socketio import SocketIO

from oxygenio.browsers import Chrome
from oxygenio.config import ConfigLoader, ROOT_PATH
from oxygenio.helpers import BrowserType, create_app


class Oxygenio:
    def __init__(self, build: bool = False) -> None:
        self.config = ConfigLoader(build)
        self.__socketio = SocketIO()
    
    def on(self, func: Callable[..., Any]):
       self.__socketio.on_event(func.__name__, func)
    
    def _get_app_url(self, host: str, port: int) -> str:
        if(self.config.is_dev_mode):
            return self.config.app_url
        return f'http://{host}:{port}'

    def _get_assets_folders(self) -> tuple[str, str]:
        if(self.config.is_dev_mode):
            return 'templates', 'static'
        
        template_folder = os.path.join(ROOT_PATH, self.config.dist_folder)
        static_folder = os.path.join(template_folder, 'assets')
        return template_folder, static_folder

    def run(self, host: str = 'localhost', port: int = 8000, browser: BrowserType = 'chrome'):
        enable = self.config.is_dev_mode

        if(browser == 'chrome' and not self.config.is_dev_mode):
            Chrome().run(url=self._get_app_url(host, port))

        app = create_app(__name__, *self._get_assets_folders())
        self.__socketio.init_app(app)
        self.__socketio.run(app, host=host, port=port, debug=enable, use_reloader=enable, log_output=False)