from gevent import monkey
monkey.patch_all()

from typing import Any, Callable, Type

from flask_socketio import SocketIO

from oxygenio.browsers import Browser, BrowserName, Chrome, Edge
from oxygenio.config import ConfigLoader
from oxygenio.helpers import create_app

browsers: dict[BrowserName, Type[Browser]] = {
    'chrome': Chrome,
    'edge': Edge
}

class Oxygenio:
    def __init__(self) -> None:
        self.config = ConfigLoader()
        self.__socketio = SocketIO(async_mode='gevent')
        self._register_default_events()
    
    @property
    def websocket(self):
        return self.__socketio

    def on(self, func: Callable[..., Any]):
       self.__socketio.on_event(func.__name__, func)
    
    def emit(self, event: str, *data: Any):
        self.__socketio.emit(event, *data)
    
    def _get_app_url(self, host: str, port: int) -> str:
        if(self.config.is_dev_mode):
            return self.config.app_url
        return f'http://{host}:{port}'

    def _register_default_events(self):
        if(not self.config.is_dev_mode):
            self.__socketio.on_event('onclose', self.__socketio.stop) # type: ignore

    def run(self, host: str = 'localhost', port: int = 15999, browser: BrowserName = 'chrome'):
        enable = self.config.is_dev_mode

        app_url = self._get_app_url(host, port)
        if(not self.config.is_dev_mode):
            browsers[browser]().run(app_url)

        app = create_app('__main__', static_folder=self.config.static_folder)
        self.__socketio.init_app(app, cors_allowed_origins=app_url)
        self.__socketio.run(
            app, 
            host=host, 
            port=port, 
            debug=enable, 
            use_reloader=enable, 
            log_output=False
        )