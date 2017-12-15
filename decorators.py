import pickle
import os
import sys
from functools import wraps
import logging

__author__ = 'Samuel Chen <samuel.net@gmail.com>'
__doc__ = """
Decorations.

@cached : Cache a function output to DB(DBCacheStorage), file(FileCacheStorage) or etc.
"""

log = logging.getLogger(__name__)

# --- decorator for cache ---
__CACHE = {}


def cached(key_or_func, expires=60):
    """
    decorator to cache a function result.
    :param key_or_func: the cached key (if specified), or the func (if not specified)
    :param expires: how many minutes will the cache expire.
    :return:
    """
    # TODO: add expires to cache.
    # TODO: add config to specify storage (may need refactor as class decorator)

    global __CACHE

    def wrap(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            storage = FileCacheStorage(sys.platform.startswith('win') and 'C:\\tmp\\' or '/tmp/')
            # storage = DBCacheStorage()
            if callable(key_or_func):
                key = func.__name__
            else:
                key = key_or_func

            if 'nocache' not in kwargs or not kwargs['nocache']:
                if key in __CACHE:
                    return __CACHE[key]
                else:
                    value = storage.load(key)
                    if value:
                        __CACHE[key] = value
                        return __CACHE[key]

            value = func(*args, **kwargs)
            __CACHE[key] = value
            storage.save(key, value)
            return __CACHE[key]

        return wrapper

    if callable(key_or_func):
        return wrap(key_or_func)
    else:
        return wrap


class CacheStorage(object):

    def _save(self, key, value):
        """override this to save to specified storage"""
        raise NotImplementedError

    def _load(self, key):
        """override this to load from specified storage"""
        raise NotImplementedError

    def save(self, key, value):
        try:
            _value = pickle.dumps(value)
            self._save(key=key, value=_value)
            log.debug('CACHED: %s.' % key)
        except Exception as err:
            log.debug('Fail to save cache for "%s". \r\n%s' % (key, str(err)))

    def load(self, key):
        value = None
        try:
            _value = self._load(key=key)
            if _value is None:
                log.debug('MISS: %s' % key)
                return None
            value = pickle.loads(_value)
            log.debug('HIT: %s loaded from cache.' % key)
        except Exception as err:
            log.debug('Fail to load cache for "%s". \r\n%s' % (key, str(err)))
        return value


class FileCacheStorage(CacheStorage):

    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            os.path.makedirs(path)

    def _load(self, key):
        fname = os.path.abspath(os.path.sep.join([self.path, key]))
        try:
            with open(fname) as f:
                value = f.read()
        except (FileExistsError, FileNotFoundError):
            value = None
        return value

    def _save(self, key, value):
        fname = os.path.abspath(os.path.sep.join([self.path, key]))
        with open(fname, 'w') as f:
            f.write(value)


class DBCacheStorage(CacheStorage):

    # TODO: DBCacheStorage need an individual access to DB

    def __init__(self):
        from backend.models.cache import DBCache        # lazy load for django
        self.DBCache = DBCache

    def _save(self, key, value):
        self.DBCache(key=key, value=value).save()

    def _load(self, key):
        try:
            return self.DBCache.objects.get(key=key).value
        except KeyError:
            return None


# ----------------------------------

def property_exception(property_name):
    """
    Decorator to add a property to Exception class. Add __init__ with property name argument also.
    :param property_name: property name to add.
    :return: decorated exception class
    """

    def rebuild_class(exception_class):

        assert issubclass(exception_class, Exception)

        class _DecoratedException(exception_class):
            def __init__(self, property_value, *args, **kwargs):
                super(_DecoratedException, self).__init__(*args, **kwargs)
                self.__property_value = property_value
                setattr(self, property_name, property(fget=fget_property))

    # def new__init__(self, property_value, *args, **kwargs):
    #     super(exception_class, self).__init__(*args, **kwargs)
    #     setattr(self, '_' + property_name, property_value)

        def fget_property(self):
            return getattr(self, '_' + property_name)

    # setattr(exception_class, '__init__', new__init__)
    # setattr(exception_class, property_name, property(fget=fget_property))

        return _DecoratedException

    return rebuild_class


# ------------------------------------


__all__ = [cached, ]
