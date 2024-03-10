from abc import ABC, abstractmethod
from subprocess import Popen, PIPE

from oxygenio.helpers import run_command

class Browser(ABC):
    @abstractmethod
    def run(self, url: str):
        pass

class Chrome(Browser):
    def __init__(self) -> None:
        self.path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    def run(self, url: str):
        Popen(
            [self.path, f'--app={url}'], 
            stdout=PIPE, stderr=PIPE, stdin=PIPE
        )

class Edge(Browser):
    def run(self, url: str):
        run_command(['start', 'msedge', '--new-window', f'--app={url}'])