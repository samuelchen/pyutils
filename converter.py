
__author__ = 'Samuel <samuel.net@gmail.com>'
__doc__ = """
Utilities for convert
"""

BIT = 1.0 / 8
BYTE = 8 * BIT
KB = 1024 * BYTE
MB = 1024 * KB
GB = 1024 * MB
TB = 1024 * GB
PB = 1024 * TB


def storage_size_to_byte(size):
    """
    Converft storage size to byte.
    Support M,MB style unit. With or W/O space. (b is bit, B is byte!!)
    e.g. "15GB", "24 m", "18.7 T"
    :param size: String of size with unit. (e.g. "15GB", "24 m", "18.7 T")
    :return:
    """

    exception = AttributeError('Incorrect format %r for parsing.' % size)

    # split size into "number" and "unit"
    size = size.strip(' ')
    x = size.split(' ')
    for i, s in enumerate(x):
        while not x[i]:
            del x[i]
    if len(x) == 1:
        idx = -1
        for i, c in enumerate(size):
            if not (c.isdigit() or c == '.'):
                idx = i
                break
        if idx > 0:
            origin_num = size[:idx]
            origin_unit = size[idx:]
        else:
            raise exception
    elif len(x) == 2:
        origin_num = x[0]
        origin_unit = x[1]
    else:
        raise exception

    try:
        num = float(origin_num)
        unit = origin_unit
    except:
        raise exception

    if num < 0:
        raise AttributeError('%r is negative size.')

    if unit in ('bits', 'bit', 'b'):
        if num != int(num):
            raise AttributeError('%r is not correct BIT number.' % origin_num)
        unit = 'BIT'
        num *= BIT
    else:
        unit = unit.lower()
        if unit in ('b', 'byte', 'bytes'):
            unit = 'BYTE'
            num *= BYTE
        elif unit in ('k', 'kb'):
            unit = 'KB'
            num *= KB
        elif unit in ('m', 'mb'):
            unit = 'MB'
            num *= MB
        elif unit in ('g', 'gb'):
            unit = 'GB'
            num *= GB
        elif unit in ('t', 'tb'):
            unit = 'TB'
            num *= TB
        elif unit in ('p', 'pb'):
            unit = 'PB'
            num *= PB
        else:
            raise exception

    return_num = num
    if 'BIT' != unit:
        if return_num != float(int(num)):
            raise AttributeError('%s (%f bytes) is not an integer Byte' % (size, num))
        else:
            return_num = int(num)

    return return_num
