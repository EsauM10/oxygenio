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

        if(browser == 'chrome' and not self.config.is_dev_mode):
            Chrome().run(url=self._get_app_url(host, port))

        app = create_app(__name__)
        self.__socketio.init_app(app)
        self.__socketio.run(app, host=host, port=port, debug=enable, use_reloader=enable, log_output=False)