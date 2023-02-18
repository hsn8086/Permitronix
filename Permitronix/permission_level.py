from typing import Union


class PermissionLevel:
    """
    Represents a permission level, which consists of a type identifier and a numeric level.
    """

    def __init__(self, level: Union[tuple[str, float], str]):
        """
        Initializes a new permission level.

        :param level: The permission level, either as a tuple containing a type identifier and a level value, or as a string
                      in the format "type_id:level".
        """
        if isinstance(level, str):
            self.load_from(level)
        else:
            self.type_id, self.level = level
            # Convert level to a float if it's not already one
            if not isinstance(self.level, float):
                self.level = float(self.level)

    def load_from(self, p_level_str: str):
        """
        Loads a permission level from a string in the format "type_id:level".

        :param p_level_str: The permission level string.
        :raises ValueError: If the string is not in the correct format.
        """
        level_tuple = p_level_str.split(':')
        if len(level_tuple) == 1:
            level_tuple.insert(0, 'Default')
        elif len(level_tuple) != 2:
            raise ValueError("Invalid permission level string.")
        self.type_id, level_str = level_tuple
        self.level = float(level_str)

    def __bool__(self):
        """
        Returns True if the permission level is greater than or equal to 0, False otherwise.

        :return: True if the permission level is greater than or equal to 0, False otherwise.
        """
        return self.level >= 0

    def __gt__(self, other: Union['PermissionLevel', str]) -> bool:
        """
        Check if this permission level is greater than another permission level.

        :param other: The other permission level to compare to.
        :raises ValueError: If the other permission level is not a string or a PermissionLevel object.
        :raises TypeError: If the two permission levels have different type identifiers.
        :return: True if this permission level is greater than the other permission level, False otherwise.
        """
        # If other is a string, create a PermissionLevel object from it
        if isinstance(other, str):
            lv = PermissionLevel(other)
        # If other is already a PermissionLevel object, use it directly
        elif isinstance(other, PermissionLevel):
            lv = other
        else:
            # If other is neither a string nor a PermissionLevel object, raise an error
            raise ValueError("other must be a PermissionLevel object or a string representation of one.")
        # Check if the type IDs of the two permission levels match
        if lv.type_id != self.type_id:
            raise TypeError('Unable to compare different types of permission levels.')
        # Check if this level is greater than the other level
        return self.level > lv.level

    def __ge__(self, other) -> bool:
        """
        Returns True if this permission level is greater than or equal to the other permission level, False otherwise.

        :param other: The other permission level to compare to.
        :return: True if this permission level is greater than or equal to the other permission level, False otherwise.
        """
        return not self < other

    def __lt__(self, other) -> bool:
        """
        Returns True if this permission level is less than the other permission level, False otherwise.

        :param other: The other permission level to compare to.
        :return: True if this permission level is less than the other permission level, False otherwise.
        """
        return not (self > other or self == other)

    def __le__(self, other) -> bool:
        """
        Returns True if this permission level is less than or equal to the other permission level, False otherwise.

        :param other: The other permission level to compare to.
        :return: True if this permission level is less than or equal to the other permission level, False otherwise.
        """
        return not (self > other)

    def __eq__(self, other: Union['PermissionLevel', str]) -> bool:
        """
        Check if two permission levels are equal.

        :param other: The other permission level to compare to.
        :return: True if the permission levels are equal, False otherwise.
        """
        # If other is a string, create a PermissionLevel object from it
        if isinstance(other, str):
            lv = PermissionLevel(other)
        # If other is already a PermissionLevel object, use it directly
        elif isinstance(other, PermissionLevel):
            lv = other
        else:
            # If other is neither a string nor a PermissionLevel object, raise an error
            raise ValueError("other must be a PermissionLevel object or a string representation of one.")
        # Check if the type IDs of the two permission levels match
        if lv.type_id != self.type_id:
            raise TypeError('Unable to compare different types of permission levels.')
        # Check if the levels of the two permission levels match
        return self.level == lv.level

    def __ne__(self, other) -> bool:
        """
        Check if two permission levels are not equal.

        :param other: The other permission level to compare to.
        :return: True if the permission levels are not equal, False otherwise.
        """
        # Simply return the negation of the equality check
        return not (self == other)

    def __str__(self):
        """
        Convert the permission level to a string representation.

        :return: A string representation of the permission level.
        """
        return f'{self.type_id}:{self.level}'
