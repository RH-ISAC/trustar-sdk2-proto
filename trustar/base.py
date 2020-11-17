from collections import MutableSet
import functools
import inspect

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


def chained(method):
    """Method decorator to allow chaining."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        return self if result is None else result
    return wrapper


def fluent(cls):
    """Class decorator to allow method chaining."""
    for name, member in cls.__dict__.iteritems():
        if inspect.isfunction(member) and name.startsWith("set_"):
            setattr(cls, name, chained(member))
    return cls


class Param:

    __slots__ = 'key', 'value'

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.key == other.key

    def __str__(self):
        # TODO html escape here
        return "{}={}".format(self.key, self.value)


class Params(MutableSet):
    """
    An orderer set, unlike regular set, add replaces old keys
    """
    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]  # sentinel node for doubly linked list
        self.map = {}  # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def _discard(self, key):
        key, prev, next = self.map.pop(key)
        prev[2] = next
        next[1] = prev

    def add(self, key):
        if key in self.map:
            self._discard(key)
        end = self.end
        curr = end[1]
        curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            self._discard(key)

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, Params):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
