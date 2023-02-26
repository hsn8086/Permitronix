import base64
import pickle
from typing import Any, Union


class DatabaseObj:
    def get(self, key) -> Any:
        ...

    def set(self, key, value) -> bool:
        ...

    def rem(self, key) -> bool:
        ...

    def exists(self, key) -> bool:
        ...


def format_data_base(db: Union['RPDB', dict]) -> DatabaseObj:
    dbo = DatabaseObj()
    db_name = type(db).__name__
    if db_name == 'RPDB':
        dbo.get = db.get
        dbo.set = db.set
        dbo.exists = db.exists
        dbo.rem = db.rem
    elif db_name == 'dict':
        class DictDBO(DatabaseObj):
            def __init__(self, db):
                self.db = db

            def get(self, key) -> Any:
                return pickle.loads(base64.b64decode(self.db[key]))

            def set(self, key, value) -> bool:
                try:
                    db[key] = base64.b64encode(pickle.dumps(value)).decode('utf8')
                    return True
                except:
                    return False

            def exists(self, key) -> bool:
                return key in db

            def rem(self, key) -> bool:
                try:
                    db.__delitem__(key)
                    return True
                except:
                    return False

        dbo = DictDBO(db)
    else:
        raise ValueError("date_base does not match the type requirements.")
    return dbo
