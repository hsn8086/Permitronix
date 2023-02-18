from typing import Union
from .permission_level import PermissionLevel
from .util.jelly import Jelly


class PermissionNode(Jelly):
    """
    A class representing a permission node that has a name and a permission level.
    """
    def __init__(self, name: str, level: Union[PermissionLevel, str] = 'Default:0'):
        """
        Initializes a new PermissionNode object.

        :param name: The name of the permission node.
        :param level: The permission level of the permission node, either as a PermissionLevel object or as a string
                      in the format "type_id:level".
        """
        super().__init__()

        # If level is not already a PermissionLevel object, create one from the provided string.
        self.level = level if isinstance(level, PermissionLevel) else PermissionLevel(level)

        self.name = name

    def __getattr__(self, item):
        """
        Delegates attribute lookup to the PermissionLevel object.

        :param item: The name of the attribute to look up.
        :return: The attribute value.
        """
        return getattr(self.level, item)

    def __bool__(self):
        """
        Returns True if the PermissionNode has a non-zero permission level, False otherwise.

        :return: True if the PermissionNode has a non-zero permission level, False otherwise.
        """
        return bool(self.level)

    def __str__(self):
        """
        Returns a string representation of the PermissionNode in the format "name:level".

        :return: A string representation of the PermissionNode.
        """
        return f'"{self.name}":"{self.level}"'
