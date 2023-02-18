from threading import Lock
from typing import Union

from RPDB.database import RPDB

from .permission_level import PermissionLevel
from .permission_node import PermissionNode
from .permission_table import PermissionTable

ver = '1.0.1'


class Permitronix:
    def __init__(self, data_base: Union[RPDB, str] = None):
        """
        Create a new permitronix instance

        :param data_base: Either the path to an existing RPDB instance or an instance of RPDB
        """
        if isinstance(data_base, str):
            self.db = RPDB(data_base)
        elif isinstance(data_base, RPDB):
            self.db = data_base
        else:
            raise ValueError("data_base must be an RPDB instance or a path to an RPDB database")

        self.todos = {}
        self.lock = Lock()

    def set_permission_table(self, obj: str, pt: PermissionTable):
        """
        Set the permission table for a given object

        :param obj: The name of the object to set the permission table for
        :param pt: The PermissionTable object to set
        """
        with self.db.enter(obj) as v:
            v.value = pt

    def get_permission_table(self, obj: str) -> PermissionTable:
        """
        Get the permission table for a given object

        :param obj: The name of the object to get the permission table for
        :return: The PermissionTable object for the specified object
        """
        if self.db.exists(obj):
            pt = self.db.get(obj)
        else:
            pt = PermissionTable(self, obj)
        pt.set_ptx(self)
        return pt

    def rem_permission_obj(self, obj: str):
        """
        Remove the permission table for a given object

        :param obj: The name of the object to remove the permission table for
        """
        if self.db.exists(obj):
            self.db.rem(obj)

    def exists(self, obj: str) -> bool:
        """
        Check if a permission table exists for a given object

        :param obj: The name of the object to check for the existence of a permission table
        :return: True if a permission table exists for the specified object, False otherwise
        """
        return self.db.exists(obj)

    def enter(self, obj):
        """
        Create a new context for a given object

        :param obj: The name of the object to create a context for
        :return: An object that can be used as a context manager
        """
        return self._with_get(self, obj)

    class _with_get:
        """
        A class that represents a context manager
        """

        def __init__(self, ptx, obj):
            """
            Create a new _with_get instance

            :param ptx: The permitronix instance that this context manager belongs to
            :param obj: The name of the object that this context manager is for
            """
            self.lock = ptx.lock
            self.ptx = ptx
            self.obj = obj

        class V:
            """
            A simple value container class
            """

            def __init__(self, v=None):
                """
                Create a new V instance

                :param v: The value to store in the V instance
                """
                self.value = v

        def __enter__(self):
            """
            Enter the context

            :return: A V object that contains the PermissionTable object for the specified object
            """
            self.lock.acquire()
            self.v = self.V()
            self.v.value = self.ptx.get_permission_table(self.obj)
            return self.v

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            This method is called when exiting the `with` block. It sets the value of the permission table
            for the object being entered in the `with` block in the database, or removes the object from
            the database if the permission table is `None`. Finally, it releases the lock held by the `with` block.
            :param exc_type: the type of the exception raised, if any
            :param exc_val: the exception object raised, if any
            :param exc_tb: the traceback object for the exception raised, if any
            :return: None
            """
            if self.v.value is not None:
                # if the permission table is not `None`, set its value in the database
                self.ptx.set_permission_table(self.obj, self.v.value)
            elif self.ptx.exists(self.obj):
                # if the permission table is `None`, and the object exists in the database, remove the object
                # from the database
                self.ptx.rem_permission_obj(self.obj)
            # release the lock held by the `with` block
            self.lock.release()
