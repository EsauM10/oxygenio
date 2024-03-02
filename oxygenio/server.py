from typing import Any, Callable

from flask_socketio import SocketIO

from oxygenio.browsers import Chrome
from oxygenio.config import ConfigLoader
from oxygenio.helpers import BrowserType, create_app


class Oxygenio:
    def __init__(self) -> None:
        self.config = ConfigLoader()
        self.__socketio = SocketIO()
    
    def on(self, func: Callable[..., Any]):
       self.__socketio.on_event(func.__name__, func)
    
    def _get_app_url(self, host: str, port: int) -> str:
        if(self.config.is_dev_mode):
            return self.config.app_url
        return f'http://{host}:{port}'

    def run(self, host: str = 'localhost', port: int = 15999, browser: BrowserType = 'chrome'):
        enable = self.config.is_dev_mode

        app_url = self._get_app_url(host, port)
        if(browser == 'chrome' and not self.config.is_dev_mode):
            Chrome().run(app_url)

        app = create_app('__main__', static_folder=self.config.static_folder)
        self.__socketio.init_app(app, cors_allowed_origins=app_url)
        self.__socketio.run(app, host=host, port=port, debug=enable, use_reloader=enable, log_output=False)