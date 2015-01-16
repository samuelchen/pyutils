#!/usr/bin/env python
# coding: utf-8

'''
Created on 2014-5-29

@author: Samuel
'''
import os
import logging
import logging.config
import traceback

TRACE = logging.NOTSET
logging.addLevelName(TRACE, 'TRACE')

class Logger(object):  
    ''' convinient log tools based on python standard logging system '''
    RED     = 1
    GREEN   = 2
    YELLOW  = 3
    BLUE    = 4
    PEARL   = 5
    SKYBLUE = 6
    WHITE   = 7

    def __init__(self, name='pyutils.logger'):
        # logConf = conf
        # if os.path.exists(logConf):
        #     logging.config.fileConfig(logConf)

        self.logger = logging.getLogger(name)

    def addHandler(self, handler):
        self.logger.addHandler(handler)

    def addFilter(self, filter):
        self.logger.addFilter(filter)

    def _fix_posix(self, color, msg):
        return "\033[3%dm%s\033[0m" % (color, msg)
    
    def _fix_win(self, color, msg):
        return msg
    
    if os.sys.platform.startswith('win'):
        fix = _fix_win
    else:
        fix = _fix_posix
        
    def _trace(self, msg, color = WHITE):
        self.logger.log(TRACE, self.fix(color, msg))

    def trace(self, msg, *args, **kwargs):
        self.logger.log(TRACE, self.fix(self.WHITE, msg), *args, **kwargs)
    
    def _debug(self, msg, color = GREEN):
        self.logger.debug(self.fix(color, msg))

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(self.fix(self.GREEN, msg), *args, **kwargs)

    def _info(self, msg, color = SKYBLUE):
        self.logger.info(self.fix(color, msg))

    def info(self, msg, *args, **kwargs):
        self.logger.info(self.fix(self.SKYBLUE, msg), *args, **kwargs)

    def _warn(self, msg, color = YELLOW):
        self.logger.warn(self.fix(color, msg))

    def warn(self, msg, *args, **kwargs):
        self.logger.warn(self.fix(self.YELLOW, msg), *args, **kwargs)

    def _error(self, msg, color = RED):
        self.logger.error(self.fix(color, msg))
        self.logger.error(self.fix(color, 'traceback: [%s]' % traceback.format_exc()))

    def error(self, msg, *args, **kwargs):
        self.logger.error(self.fix(self.RED, msg), *args, **kwargs)
        self.logger.error(self.fix(self.RED, 'traceback: [%s]' % traceback.format_exc()))
    
    def _fatal(self, msg, color = PEARL):
        self.logger.critical(self.fix(color, msg))
        self.logger.critical(self.fix(color, 'traceback: [%s]' % traceback.format_exc()))

    def fatal(self, msg, *args, **kwargs):
        self.logger.critical(self.fix(self.PEARL, msg), *args, **kwargs)
        self.logger.critical(self.fix(self.PEARL, 'traceback: [%s]' % traceback.format_exc()))

log = Logger('pyutils')

if __name__ == '__main__':
    log = Logger('pyutils')

    for i in xrange(10000):
        log.debug('debug message %d' % i)
        log.warn('warn message %d' % i)
