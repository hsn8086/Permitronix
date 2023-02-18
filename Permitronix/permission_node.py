from typing import Union

from .permission_level import PermissionLevel
from .util.jelly import Jelly


class PermissionNode(Jelly):
    def __init__(self, name: str, level: Union[PermissionLevel, str] = 'Default:0'):
        super().__init__()

        self.level = level if isinstance(level, PermissionLevel) else PermissionLevel(level)

        self.name = name

    def __getattr__(self, item):
        return getattr(self.level, item)

    def __bool__(self):
        return bool(self.level)

    def __str__(self):
        return f'"{self.name}":"{self.level}"'
