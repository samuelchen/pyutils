from collections import Mapping, MutableMapping, Iterable, OrderedDict
import threading

__author__ = 'Samuel Chen <samuel.net@gmail.com>'
__doc__ = """
Utilities to enhance python language.
"""


class Enum(Mapping):
    """
    Readonly enumeration.
    e.g. ::
    my_enum = Enum(a=1, b=2)
    my_enum = Enum({
            a: 1,
            "B": "two",
            })
    my_enum = Enum([
            (a, 1),
            ("b", "two),
            ])
    my_enum.a = 1
    my_enum['b'] = "two"
    ::
    """

    def __init__(self, iterable=None, **kwargs):
        super(Enum, self).__init__()
        self._enums = {}
        self._lock = threading.RLock()
        self._update(iterable, **kwargs)

    def _update(self, iterable=None, **kwargs):
        if iterable is not None:
            if isinstance(iterable, Mapping):
                items = iterable.items()
            elif isinstance(iterable, Iterable):
                items = iterable
            else:
                raise TypeError('%s is not Iterable' % str(iterable))

            for k, v in items:
                with self._lock:
                    self._enums[k] = v
                    setattr(self, k, v)
        for k, v in kwargs.items():
            with self._lock:
                self._enums[k] = v
                setattr(self, k, v)

    def __len__(self):
        return len(self._enums)

    def __getitem__(self, key):
        return self._enums[key]

    def __iter__(self):
        for key in self._enums:
            yield (key, self._enums[key])


class MutableEnum(Enum, MutableMapping):
    """
    Mutable enumeration. Inherits from Enum.
    """

    def __setitem__(self, key, value):
        with self._lock:
            self._enums[key] = value
            setattr(self, key, value)

    def __delitem__(self, key):
        with self._lock:
            del self._enums[key]
            delattr(self, key)

    def pop(self, key, default=None):
        with self._lock:
            value = self._enums.pop(key)
            delattr(self, key)
            return value

    def popitem(self):
        with self._lock:
            k, v = self._enums.popitem()
            if k:
                delattr(self, k)
            return v

    def clear(self):
        with self._lock:
            for k in self._enums.keys():
                delattr(self, k)
            self._enums.clear()

    def update(self, iterable=None, **kwargs):
        self._update(iterable, **kwargs)


class SingletonBase(object):
    """
    Base class for creating singleton class
    """

    # class level variables
    __instance = None
    __lock = threading.Lock()
    __ref_count = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__lock.acquire()
            cls.__instance = object.__new__(cls)
            cls.__ref_count += 1
            cls.__lock.release()
        return cls.__instance

    def __del__(self):
        cls = self.__class__
        if None == cls.__instance:
            return

        cls.__lock.acquire()
        cls.__ref_count -= 1
        if 0 == cls.__ref_count and None != cls.__instance:
            cls.__instance.close()
            cls.__instance = None
        cls.__lock.release()


class PropertyDict(OrderedDict):
    """
    A class based ordered dict and supports dot notation.
    e.g. Either "obj.name" or "obj['name']" works
    """

    # def __getitem__(self, key):
    #     if self.fail_as_none and key not in self.keys():
    #         return None
    #     return super(PropertyDict, self).__getitem__(key)

    def __getattr__(self, key):
        if key in self.keys():
            return self[key]
        else:
            return super(PropertyDict, self).__getattribute__(key)

    def __setattr__(self, key, value):
        if key in self.keys():
            return super(PropertyDict, self).__setitem__(key, value)
        else:
            return super(PropertyDict, self).__setattr__(key, value)

    def __delattr__(self, key):
        if key in self.keys():
            return super(PropertyDict, self).__delitem__(key)
        else:
            return super(PropertyDict, self).__delattr__(key)

    # __fail_as_none = False
    #
    # @property
    # def fail_as_none(self):
    #     return self.__fail_as_none
    #
    # @fail_as_none.setter
    # def fail_as_none(self, value):
    #     assert value is bool
    #     self.__fail_as_none = value