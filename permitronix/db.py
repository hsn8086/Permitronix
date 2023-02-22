from typing import Any, Union


class DatabaseObj:
    def get(self, key) -> Any:
        ...

    def set(self, key, value) -> bool:
        ...


def format_data_base( db: Union['RPDB', dict]) -> DatabaseObj:
    dbo = DatabaseObj()
    db_name = type(db).__name__
    if db_name == 'RPDB':
        dbo.get = db.get
        dbo.set = db.set
    return dbo
