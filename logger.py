import os
import logging
import logging.config
import traceback
from termcolor import colored

__author__ = 'Samuel Chen <samuel.net@gmail.com>'
__doc__ = """
Utilities/Enhancement for python logging.
"""

logging.TRACE = logging.DEBUG - 5
logging.addLevelName(logging.TRACE, 'TRACE')


class ColorFormatter(logging.Formatter):
    """
    A colorful handler for python logging

    ''color reference: https://pypi.python.org/pypi/termcolor
    'LEVEL': ('fg-color', 'bg-color', ['attr1', 'attr2', ...])''

    ### Color config
    ::
    _colors = {
        'TRACE': ('grey', None, []),
        'DEBUG': ('grey', None, ['bold']),
        'INFO': (None, None, []),
        'WARNING': ('yellow', None, []),
        'ERROR': ('red', None, []),
        'CRITICAL': ('red', 'white', []),

    }
    ::

    ### Dict style log config:
    ::
    LOGGING = {
        ...
        'formatters': {
            'colored': {
                'format': '%(levelname)-7s [%(asctime)s] %(name)-30s [%(lineno)d] %(message)s',
                '()': 'utils.logger.ColorFormatter',
                'colors': {
                    'TRACE': ('grey', None, []),
                    'DEBUG': ('grey', None, ['bold']),
                    'INFO': (None, None, []),
                    'WARNING': ('yellow', None, []),
                    'ERROR': ('red', None, []),
                    'CRITICAL': ('red', 'white', []),

                }
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'colored'
            },
        },
        'loggers': {
            'foo': {
                'handlers': ['console'],
                'level': 'WARNING',
            },
        },
        ...
    }
    ::
    """

    def __init__(self, fmt=None, datefmt=None, colors=None):
        self.colors = colors
        super(ColorFormatter, self).__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):

        s = super(ColorFormatter, self).format(record)

        lvlname = record.levelname
        if lvlname in self.colors:
            fg, bg, attrs = self.colors[lvlname]
            return colored(s, fg, bg, attrs)
        else:
            print('Log %r has no color defined.' % lvlname)
            return s


class Logger(object):
    """
    Convenience log tool based on python logging
    ** Use ColoredFormatter instead of using this **
    """

    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PEARL = 5
    SKYBLUE = 6
    WHITE = 7

    def __init__(self, name=None):
        self.logger = logging.getLogger(name)

    def addHandler(self, handler):
        self.logger.addHandler(handler)

    def addFilter(self, filter):
        self.logger.addFilter(filter)

    def _fix_posix(self, color, msg):
        return "\033[3%dm %s \033[0m" % (color, msg)

    def _fix_win(self, color, msg):
        return msg

    if os.sys.platform.startswith('win'):
        fix = _fix_win
    else:
        fix = _fix_posix

    def _trace(self, msg, color=WHITE):
        self.logger.log(logging.TRACE, self.fix(color, msg))

    def trace(self, msg, *args, **kwargs):
        self.logger.log(logging.TRACE, self.fix(self.WHITE, msg), *args, **kwargs)

    def _debug(self, msg, color=BLACK):
        self.logger.debug(self.fix(color, msg))

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(self.fix(self.BLACK, msg), *args, **kwargs)

    def _info(self, msg, color=BLUE):
        self.logger.info(self.fix(color, msg))

    def info(self, msg, *args, **kwargs):
        self.logger.info(self.fix(self.BLUE, msg), *args, **kwargs)

    def _warn(self, msg, color=YELLOW):
        self.logger.warn(self.fix(color, msg))

    def warn(self, msg, *args, **kwargs):
        self.logger.warn(self.fix(self.YELLOW, msg), *args, **kwargs)

    def _error(self, msg, color=RED):
        self.logger.error(self.fix(color, msg))

    def error(self, msg, *args, **kwargs):
        self.logger.error(self.fix(self.RED, msg), *args, **kwargs)

    def _critical(self, msg, color=PEARL):
        self.logger.critical(self.fix(color, msg))

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(self.fix(self.PEARL, msg), *args, **kwargs)

    def _exception(self, msg, color=RED):
        self.logger.error(self.fix(color, msg))
        self.logger.exception(self.fix(color, 'traceback: [%s]' % traceback.format_exc()))

    def exception(self, msg, *args, **kwargs):
        self.logger.error(self.fix(self.RED, msg), *args, **kwargs)
        self.logger.exception(self.fix(self.RED, 'traceback: [%s]' % traceback.format_exc()))


if __name__ == '__main__':
    logging.config.fileConfig('logger.conf.sample')
    log = Logger(__name__)

    for i in xrange(3):
        log.trace('trace message %d' % i)
        log.debug('debug message %d' % i)
        log.info('info message %d' % i)
        log.warn('warn message %d' % i)
        log.error('error message %d' % i)
        log.fatal('fatal message %d' % i)

        log._trace('trace message %d' % i, log.SKYBLUE)
        log._debug('debug message %d' % i, log.GREEN)
        log._info('info message %d' % i, log.BLUE)
        log._warn('warn message %d' % i, log.YELLOW)
        log._error('error message %d' % i, log.PEARL)
        log._fatal('fatal message %d' % i, log.RED)

