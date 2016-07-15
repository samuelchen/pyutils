from time import sleep
import logging

__author__ = 'Samuel Chen <samuel.net@gmail.com>'
__date__ = '2016/7/4 17:08'
__doc__ = """
Utilities for robust programming.
"""

log = logging.getLogger(__name__)


def retry(func, args=[], kwargs={}, times=3, interval=3, timeout=30):
    """
    Execute a function for "times" with "interval" (retry "times - 1")
    If the func does not raise any exception, we think it executed succefully.
    :param func: The func to call
    :param args: argument list (list)
    :param kwargs: key-value naming arguments dictionary (dict)
    :param times: How many times to retry
    :param interval: Retry interval (seconds)
    :param timeout: [NotImplemented] Timeout for each round executing. (seconds)
    :return: The func return value.
    """

    rc = None
    succeed = False
    count = 1
    while not succeed and count <= times:
        try:
            rc = func(*args, **kwargs)
            succeed = True
        except Exception as err:
            log.exception(err)
            log.info('Retry executing %s ... %d' % (str(func), count))
        count += 1
        sleep(interval)

    return rc


__all__ = [retry, ]