import json
import os
import tempfile
from abc import ABC, abstractmethod
from subprocess import Popen
from typing import Literal

BrowserName = Literal['chrome', 'edge']

def _create_isolated_profile(prefix: str) -> str:
    user_data_dir = tempfile.mkdtemp(prefix=prefix)
    profile_dir = os.path.join(user_data_dir, 'Default')
    os.makedirs(profile_dir, exist_ok=True)

    preferences_path = os.path.join(profile_dir, 'Preferences')
    with open(preferences_path, mode='w') as file:
        json.dump({'translate': {'enabled': False}}, file)

    return user_data_dir

class Browser(ABC):
    @abstractmethod
    def run(self, url: str) -> Popen:
        pass

class Chrome(Browser):
    def __init__(self) -> None:
        self.path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

    def run(self, url: str) -> Popen:
        user_data_dir = _create_isolated_profile('oxygenio-chrome-')
        return Popen(
            [
                self.path,
                f'--user-data-dir={user_data_dir}',
                '--disable-features=Translate,TranslateUI',
                f'--app={url}'
            ]
        )

class Edge(Browser):
    def __init__(self) -> None:
        self.path = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'

    def run(self, url: str) -> Popen:
        user_data_dir = _create_isolated_profile('oxygenio-edge-')
        return Popen(
            [
                self.path,
                f'--user-data-dir={user_data_dir}',
                '--disable-features=Translate,TranslateUI',
                '--new-window',
                f'--app={url}'
            ]
        )