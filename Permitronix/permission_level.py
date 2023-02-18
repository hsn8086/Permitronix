from typing import Union


class PermissionLevel:
    def __init__(self, level: Union[tuple[str, float], str]):
        if isinstance(level, str):
            self.load_from(level)
        else:
            self.type_id, self.level = level
            if not isinstance(self.level, float):
                self.level = float(self.level)

    def load_from(self, p_level_str: str):
        level_tuple = p_level_str.split(':')
        if len(level_tuple) == 1:
            level_tuple.insert(0, 'Default')
        elif len(level_tuple) != 2:
            raise ValueError()
        self.type_id, level_str = level_tuple
        self.level = float(level_str)

    def __bool__(self):
        return self.level >= 0

    def __gt__(self, other: Union['PermissionLevel', str]) -> bool:
        if isinstance(other, str):
            lv = PermissionLevel(other)
        elif isinstance(other, PermissionLevel):
            lv = other
        else:
            raise ValueError()
        if lv.type_id != self.type_id:
            raise TypeError('Unable to compare different types of permission levels.')
        return self.level > lv.level

    def __ge__(self, other) -> bool:
        return not self < other

    def __lt__(self, other) -> bool:
        return not (self > other or self == other)

    def __le__(self, other) -> bool:
        return not self > other

    def __ne__(self, other) -> bool:
        return not self == other

    def __eq__(self, other: Union['PermissionLevel', str]) -> bool:
        if isinstance(other, str):
            lv = PermissionLevel(other)
        elif isinstance(other, PermissionLevel):
            lv = other
        else:
            raise ValueError()
        if lv.type_id != self.type_id:
            raise TypeError('Unable to compare different types of permission levels.')
        return self.level == lv.level

    def __str__(self):
        return f'{self.type_id}:{self.level}'
