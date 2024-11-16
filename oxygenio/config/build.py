from dataclasses import dataclass
from typing import Any

@dataclass
class BuildConfig:
    mode: str
    app_url: str
    dev_command: str
    build_command: str
    app: str
    dist_folder: str
    static_folder: str

    @staticmethod
    def from_dict(payload: dict[str, Any]):
        return BuildConfig(
            mode = 'build' if(payload['mode'] == 'build') else 'dev',
            app_url = str(payload['appURL']),
            dev_command = str(payload['devCommand']),
            build_command = str(payload['buildCommand']),
            app = str(payload['frontendApp']),
            dist_folder = str(payload['distFolder']),
            static_folder = str(payload['staticFolder'])
        )
        
    @property
    def to_dict(self) -> dict[str, str]:
        return {
            'mode': self.mode,
            'appURL': self.app_url,
            'devCommand': self.dev_command,
            'buildCommand': self.build_command,
            'frontendApp': self.app,
            'distFolder': self.dist_folder,
            'staticFolder': self.static_folder
        }