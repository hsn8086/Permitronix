import re
from typing import Union

import permitronix
from .permission_node import PermissionNode
from .util.jelly import Jelly


class PermissionTable(Jelly):
    """
    A class that represents a table of permission nodes.
    """

    def __init__(self, ptx: permitronix, name: str):
        """
        Initialize a new PermissionTable object.

        :param ptx: a permitronix object
        :param name: the name of the permission table
        """
        super().__init__()
        self.name = name
        self.__ptx = ptx
        self.bases = set()
        self.nodes = {}

    def set_ptx(self, ptx: permitronix):
        """
        Set the permitronix object.

        :param ptx: a permitronix object
        """
        self.__ptx = ptx

    def add_base_pt(self, pt: Union['PermissionTable', str]):
        """
        Add a base permission table.

        :param pt: a PermissionTable object or the name of a permission table
        """
        self.bases.add(pt.name if isinstance(pt, PermissionTable) else pt)

    def rem_base_pt(self, pt: Union['PermissionTable', str]):
        """
        Remove a base permission table.

        :param pt: a PermissionTable object or the name of a permission table
        """
        self.bases.remove(pt.name if isinstance(pt, PermissionTable) else pt)

    def set_permission(self, pn: PermissionNode):
        """
        Set a permission node.

        :param pn: a PermissionNode object
        """
        self.nodes[pn.name] = pn

    def rem_permission(self, pn_name: str):
        """
        Remove a permission node.

        :param pn_name: the name of the permission node
        """
        self.nodes.pop(pn_name)

    def get_permission(self, pn_name: str):
        """
        Get a permission node by name.

        :param pn_name: the name of the permission node
        :return: a PermissionNode object or None
        """
        if pn_name in self.nodes:
            return self.nodes[pn_name]
        else:
            for _, v in self.nodes.items():
                if re.fullmatch(v.name, pn_name):
                    return v
            for i in self.bases:
                pn = self.__ptx.get_permission_table(i).get_permission(pn_name)
                if pn is not None:
                    return pn
            return None

    def get_permission_bool(self, pn_name: str):
        """
        Get a boolean value indicating whether a permission node exists.

        :param pn_name: the name of the permission node
        :return: a boolean value
        """
        return bool(self.get_permission(pn_name))

    def __gt__(self, pn: PermissionNode):
        """
        Check if a permission node is greater than another permission node.

        :param pn: a PermissionNode object
        :return: a boolean value
        """
        self_pn = self.get_permission(pn.name)
        if self_pn is not None:
            return self_pn > pn
        else:
            return False

    def __lt__(self, pn: PermissionNode):
        """
        Check if a permission node is less than another permission node.

        :param pn: a PermissionNode object
        :return: a boolean value
        """
        return not self >= pn

    def __eq__(self, pn: PermissionNode):
        """
        Returns True if the PermissionTable contains the PermissionNode pn.
        :param pn: PermissionNode to compare with.
        :return: True if the PermissionTable contains the PermissionNode pn, False otherwise.
        """
        return pn.name in self.nodes and self.nodes[pn.name] == pn

    def __ge__(self, pn: PermissionNode):
        """
        Returns True if the PermissionTable is greater than or equal to the PermissionNode pn.
        :param pn: PermissionNode to compare with.
        :return: True if the PermissionTable is greater than or equal to the PermissionNode pn, False otherwise.
        """
        return self > pn or self == pn

    def __le__(self, pn: PermissionNode):
        """
        Returns True if the PermissionTable is less than or equal to the PermissionNode pn.
        :param pn: PermissionNode to compare with.
        :return: True if the PermissionTable is less than or equal to the PermissionNode pn, False otherwise.
        """
        return not self > pn

    def __ne__(self, pn: PermissionNode):
        """
        Returns True if the PermissionTable does not contain the PermissionNode pn.
        :param pn: PermissionNode to compare with.
        :return: True if the PermissionTable does not contain the PermissionNode pn, False otherwise.
        """
        return not self == pn

    def __str__(self):
        """
        Returns a string representation of the PermissionTable.
        :return: String representation of the PermissionTable.
        """
        return "bases:\n{}\nnodes:{}".format(''.join([f'\n\t{str(i)}' for i in self.bases]),
                                             ''.join(['\n\t' + str(self.get_permission(i)) for i in self.nodes]))
