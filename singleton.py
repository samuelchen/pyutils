#!/usr/bin/env python
# coding: utf-8
__author__ = 'Samuel Chen <samuel.net@gmail.com>'

'''
singleton module description

Created on 1/7/2015
'''

import threading
from logger import log

class SingletonBase(object):

    # class level variables
    __instance = None
    __lock = threading.Lock()
    __ref_count = 0

    def __new__(cls, *args, **kwargs):
        if None == cls.__instance:
            cls.__lock.acquire()
            cls.__instance = object.__new__(cls)
            cls.__ref_count += 1
            cls.__lock.release()
            log.info('%s instance created.' % cls)
        return cls.__instance

    def __del__(self):
        cls = self.__class__
        if None == cls.__instance:
            return

        cls.__lock.acquire()
        cls.__ref_count -= 1
        log.info('%s instance reference count decreased. count=%d' % (cls, cls.__ref_count))
        if 0 == cls.__ref_count and None != cls.__instance:
            cls.__instance.close()
            cls.__instance = None
            log.info('%s instance is removed.')
        cls.__lock.release()
