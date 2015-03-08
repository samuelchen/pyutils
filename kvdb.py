#!/usr/bin/env python
# coding: utf-8
__author__ = 'Samuel Chen <samuel.net@gmail.com>'

'''
kvdb module description

Created on 3/8/2015
'''

from pyutils import Logger
log = Logger(__name__)

class KVDB(object):
    '''
    The key-value storage wrapper. You need to pass-in the required functions as callbacks to use it.
    '''

    def __init__(self, put_callback, get_callback, scan_callback):
        '''
        Initialize a KVDB wrapper object.

        :param put_callback: The "put" callback is used to storage a pair of key-value data. Should accept (key, value, meta) arguments
        :param get_callback: The "get" callback is used to retrieve data by given key. Should accept (key, meta) arguments
        :param scan_callback: The "scan" callback is used to scan keys. Should accept (pattern, meta) arguments. "pattern" is the wild-mask/regular-expression for "key".
        :return: Initialized KVDB wrapper object
        '''

        self._cb_put = put_callback
        self._cb_get = get_callback
        self._cb_scan = scan_callback
        assert (put_callback and get_callback and scan_callback)


    def put(self, key, value, meta=''):
        rc = None
        try:
            rc = self._cb_put(key, value, meta)
        except Exception, e:
            log.exception('Fail to save data(key="%s") in KVDB.' % key, e)

        return rc

    def get(self, key, meta=''):
        rc = None
        try:
            rc = self._cb_get(key, meta)
        except Exception, e:
            log.exception('Fail to load data(key="%s") from KVDB.' % key, e)

        return rc

    def scan(self, pattern, meta=''):
        rc = None
        try:
            rc = self._cb_scan(pattern, meta)
        except Exception, e:
            log.exception('Fail to scan data(pattern="%s") from KVDB.' % pattern, e)

        return rc