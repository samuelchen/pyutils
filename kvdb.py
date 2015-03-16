#!/usr/bin/env python
# coding: utf-8
__author__ = 'Samuel Chen <samuel.net@gmail.com>'

'''
kvdb module description

Created on 3/8/2015
'''

from pyutils import Logger
log = Logger(__name__)

class KVDBWrapper(object):
    '''
    The key-value storage wrapper. You need to pass-in the required functions as callbacks to use it.
    '''

    def __init__(self, kvdb_class, **kwargs):
        '''
        Initialize a KVDB wrapper object.

        :param kvdb_class: The class for wrapped KVDB client. It will be used to initialize an client object. The object must have one or more of the following methods.
            - "set" method is used to storage a pair of key-value data. Should accept (key, value, meta) arguments
            - "get" method is used to retrieve data by given key. Should accept (key, meta) arguments
            - "scan" method is used to scan keys. Should accept (kwargs) arguments.
            - "scanv" method is used to scan key-values. Should accept (kwargs) arguments.
        :return: Initialized KVDB wrapper object
        '''

        self.client = object.__new__(kvdb_class, **kwargs)
        self.client.__init__(**kwargs)
        assert (self.client)

    def info(self):
        rc = ''
        try:
            rc = self.client.info()
        except Exception, e:
            log.exception('Fail to get db info.')
        return rc

    def set(self, key, value, **kwags):
        rc = None
        try:
            rc = self.client.set(key, value, **kwags)
        except Exception, e:
            log.exception('Fail to save data in KVDB. (key="%s")' % key)

        return rc

    def get(self, key, **kwargs):
        rc = None
        try:
            rc = self.client.get(key, **kwargs)
        except Exception, e:
            log.exception('Fail to get data from KVDB. (key=%s)' % key)

        return rc

    def delete(self, key, **kwargs):
        rc = None
        try:
            rc = self.client.delete(key, **kwargs)
        except Exception, e:
            log.exception('Fail to delete data from KVDB. (key=%s)' % key)

        return rc

    def exist(self, key, **kwargs):
        rc = None
        try:
            rc = self.client.exist(key, **kwargs)
        except Exception, e:
            log.exception('Fail to get data from KVDB. (key=%s)' % key)

        return rc

    def scan(self, cursor, count, **kwargs):
        rc = None
        try:
            rc = self.client.scan(cursor, count, **kwargs)
        except Exception, e:
            log.exception('Fail to retrieve keys data from KVDB. (kwargs="%s")' % kwargs)

        return rc


    def scanv(self, cursor, count, **kwargs):
        rc = None
        try:
            rc = self.client.scanv(cursor, count, **kwargs)
        except Exception, e:
            log.exception('Fail to retrieve key-values data from KVDB. (kwargs="%s")' % kwargs)

        return rc