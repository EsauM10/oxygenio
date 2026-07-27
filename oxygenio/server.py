from gevent import monkey
monkey.patch_all()

import gevent
import socket
import time
from subprocess import Popen
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

    def _watch_browser(self, process: Popen):
        process.wait()
        self.__socketio.stop()

    def _wait_until_listening(self, host: str, port: int, timeout: float = 10):
        deadline = time.time() + timeout
        while(time.time() < deadline):
            try:
                with socket.create_connection((host, port), timeout=0.5):
                    return
            except OSError:
                gevent.sleep(0.1)
        raise RuntimeError(f'Server did not start listening on {host}:{port} in time')

    def run(self, host: str = '127.0.0.1', port: int = 15999, browser: BrowserName = 'chrome'):
        enable = self.config.is_dev_mode

        app_url = self._get_app_url(host, port)
        app = create_app('__main__', static_folder=self.config.static_folder)
        self.__socketio.init_app(app, cors_allowed_origins=app_url)

        server = gevent.spawn(
            self.__socketio.run,
            app,
            host=host,
            port=port,
            debug=enable,
            use_reloader=enable,
            log_output=False
        )

        if(not self.config.is_dev_mode):
            self._wait_until_listening(host, port)
            process = browsers[browser]().run(app_url)
            gevent.spawn(self._watch_browser, process)

        server.join()