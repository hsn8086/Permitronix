import re
from typing import Union

import Permitronix
from .permission_node import PermissionNode
from .util.jelly import Jelly


class PermissionTable(Jelly):
    def __init__(self, ptx: Permitronix, name: str):
        super().__init__()
        self.name = name
        self.__ptx = ptx
        self.bases = set()
        self.nodes = {}

    def set_ptx(self, ptx):
        self.__ptx = ptx

    def add_base_pt(self, pt: Union['PermissionTable', str]):
        self.bases.add(pt.name if isinstance(pt, PermissionTable) else pt)

    def rem_base_pt(self, pt: Union['PermissionTable', str]):
        self.bases.remove(pt.name if isinstance(pt, PermissionTable) else pt)

    def set_permission(self, pn: PermissionNode):
        self.nodes[pn.name] = pn

    def rem_permission(self, pn_name: str):
        self.nodes.pop(pn_name)

    def get_permission(self, pn_name: str):

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
        return bool(self.get_permission(pn_name))

    def __gt__(self, pn: PermissionNode):
        self_pn = self.get_permission(pn.name)
        if self_pn is not None:
            return self_pn > pn
        else:
            return False

    def __lt__(self, pn: PermissionNode):
        return not self >= pn

    def __eq__(self, pn: PermissionNode):
        self_pn = self.get_permission(pn.name)
        if self_pn is not None:
            return self_pn == pn
        else:
            return False

    def __ge__(self, pn: PermissionNode):
        return self > pn or self == pn

    def __le__(self, pn: PermissionNode):
        return not self > pn

    def __ne__(self, pn: PermissionNode):
        return not self == pn

    def __str__(self):
        return "bases:\n{}\nnodes:{}".format(''.join([f'\n\t{str(i)}' for i in self.bases]),
                                             ''.join(['\n\t' + str(self.get_permission(i)) for i in self.nodes]))
