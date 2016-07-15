from . import strutil
from .kvdb import KVDBWrapper
from .decorators import cached
from .robust import retry
from .logger import ColorFormatter
from .langutil import Enum, MutableEnum, SingletonBase


__author__ = 'Samuel <samuel.net@gmail.com>'
__version__ = '1.0.0'
__doc__ = """
The python convenience utilities.
"""
__all__ = [
    SingletonBase,
    strutil,
    KVDBWrapper,
    retry, cached,
    ColorFormatter,
    Enum, MutableEnum,
]
