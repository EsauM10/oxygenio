from dataclasses import dataclass
from typing import Any


@dataclass
class WindowConfig:
    title: str
    width: int
    height: int
    resizable: bool
    maximize: bool

    @staticmethod
    def from_dict(window_data: dict[str, Any]):
        data = window_data.get('window') or {}
    
        return WindowConfig(
            title=data.get('title') or 'Oxygen App',
            width=int(data.get('width') or 600),
            height=int(data.get('height') or 400),
            resizable=bool(data.get('resizable')),
            maximize=bool(data.get('maximize'))
        )
