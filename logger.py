#!/usr/bin/env python
# coding: utf-8

'''
Created on 2014-5-29

@author: Samuel
'''
import os
import sys
import logging
import logging.config
import traceback
import setting

TRACE = logging.NOTSET
logging.addLevelName(TRACE, 'TRACE')

formatter = logging.Formatter(
                  fmt='[%(asctime)s] [%(process)d] [%(name)-8s] [%(levelname)-5s] - %(message)s',
                  datefmt='%y-%m-%d %H:%M:%S')

consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(logging.NOTSET)

fileHandler = logging.handlers.RotatingFileHandler(setting.log.file, 'a')
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.INFO)

class Logger(object):  
    ''' convinient log tools based on python standard logging system '''
    RED     = 1
    GREEN   = 2
    YELLOW  = 3
    BLUE    = 4
    PEARL   = 5
    SKYBLUE = 6
    WHITE   = 7

    def __init__(self):
#         logConf = setting.log_conf
#         if os.path.exists(logConf):
#             logging.config.fileConfig(logConf)

        self.logger = logging.getLogger("leaf")
        self.logger.addHandler(consoleHandler)
        self.logger.addHandler(fileHandler)

    def _fix_posix(self, color, msg):
        return "\033[3%dm%s\033[0m" % (color, msg)
    
    def _fix_win(self, color, msg):
        return msg
    
    if os.sys.platform.startswith('win'):
        fix = _fix_win
    else:
        fix = _fix_posix
        
    def trace(self, msg, color = WHITE):
        self.logger.log(TRACE, self.fix(color, msg))
    
    def debug(self, msg, color = GREEN):
        self.logger.debug(self.fix(color, msg))

    def info(self, msg, color = SKYBLUE):
        self.logger.info(self.fix(color, msg))
        
    def warn(self, msg, color = YELLOW):
        self.logger.warn(self.fix(color, msg))

    def error(self, msg, color = RED):
        self.logger.error(self.fix(color, msg))
        self.logger.error(self.fix(color, 'traceback: [%s]' % traceback.format_exc()))
    
    def fatal(self, msg, color = PEARL):
        self.logger.critical(self.fix(color, msg))
        self.logger.critical(self.fix(color, 'traceback: [%s]' % traceback.format_exc()))
        
log = Logger()

