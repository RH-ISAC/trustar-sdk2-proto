from enum import Enum


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class Methods(AutoNumber):
    POST = ()
    GET = ()
    DELETE = ()
    UPDATE = ()
    PUT = ()


class Param:

    __slots__ = '__key', 'value'

    def __init__(self, key, value):
        self.__key = key
        self.value = value

    def __hash__(self):
        return hash(self.__key)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.__key == other.__key

    def __str__(self):
        # TODO html escape here
        return "{}={}".format(self.__key, self.value)
