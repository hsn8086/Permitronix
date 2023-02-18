from threading import Lock
from typing import Union

from RPDB.database import RPDB

from .permission_level import PermissionLevel
from .permission_node import PermissionNode
from .permission_table import PermissionTable

ver = '0.0.1'


class Permitronix:
    def __init__(self, data_base: Union[RPDB, str] = None):
        if isinstance(data_base, str):
            self.db = RPDB(data_base)
        elif isinstance(data_base, RPDB):
            self.db = data_base
        else:
            raise ValueError()

        self.todos = {}
        self.lock = Lock()
        '''threading.Thread(target=self._operation_thread, name='op_thread')

    def _operation_thread(self):
        while True:
            self.lock.acquire()
            for k, task in copy.deepcopy(self.todos).items():
                self.todos.pop(k)
                if task['type'] == 'set':
                    self.db.set(task['key'], task['value'])
                elif task['type'] == 'rem':
                    self.db.rem(task['key'])
            self.lock.release()
            sleep(0.1)

    def _add_task(self, **kwargs):
        self.lock.acquire()
        self.todos[uuid4()] = kwargs
        self.lock.release()'''

    def set_permission_table(self, obj: str, pt: PermissionTable):

        with self.db.enter(obj) as v:
            v.value = pt

    def get_permission_table(self, obj: str) -> PermissionTable:
        if self.db.exists(obj):
            pt = self.db.get(obj)
        else:
            pt = PermissionTable(self, obj)
        pt.set_ptx(self)

        return pt

    def rem_permission_obj(self, obj: str):
        if self.db.exists(obj):
            self.db.rem(obj)

    def exists(self, obj: str) -> bool:
        return self.db.exists(obj)

    def enter(self, obj):
        return self._with_get(self, obj)

    class _with_get:
        def __init__(self, ptx, obj):
            self.lock = ptx.lock
            self.ptx = ptx
            self.obj = obj

        class V:
            def __init__(self, v=None):
                self.value = v

        def __enter__(self):
            self.lock.acquire()
            self.v = self.V()
            self.v.value = self.ptx.get_permission_table(self.obj)
            return self.v

        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.v.value is not None:
                self.ptx.set_permission_table(self.obj, self.v.value)
            elif self.ptx.exists(self.obj):
                self.ptx.rem_permission_obj(self.obj)
            self.lock.release()
