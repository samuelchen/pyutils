#!/usr/bin/env python
# coding: utf-8

"""
JSON patch

https://hynek.me/articles/serialization/
# >>> json.dumps({"msg": "hi", "ts": datetime.now()},
# ...            default=to_serializable)
# '{"ts": "2016-08-20T13:08:59.153864Z", "msg": "hi"}'
"""

from datetime import datetime
from functools import singledispatch

@singledispatch
def to_serializable(val):
    """Used by default."""
    return str(val)

@to_serializable.register(datetime)
def ts_datetime(val):
    """Used if *val* is an instance of datetime."""
    # return val.isoformat() + "Z"
    # datetime.strptime('Mon, 23 May 2016 08:30:15 GMT', '%a, %d %B %Y %H:%M:%S GMT')
    return val.strftime('%Y-%m-%d %H:%M:%S.%f%z')
    #'YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]'