import re

__author__ = 'Samuel <samuel.net@gmail.com>'
__doc__ = """
Utilities for convert
"""


re_storage_size = re.compile(r'[\D\.]+|\W+')
def storage_size_to_byte(size):
    """
    Converft storage size to byte.
    Support M,MB style unit. With or W/O space. (b is bit, B is byte!!)
    e.g. "15GB", "24 m", "18.7 T"
    :param size:
    :return:
    """
    assert isinstance(size, str)
    exception = AttributeError('Incorrect format %r for parsing.' % size)

    bit = 1/8
    B = 8 * bit
    KB = 1024 * B
    MB = 1024 * KB
    GB = 1024 * MB
    TB = 1024 * GB
    PB = 1024 * TB

    size = size.strip(' ')
    x = size.split(' ')
    if len(x) == 1:
        x = re_storage_size.split(size, 1)
    if len(x) != 2:
        raise exception

    print(x)

    num = x[0]
    unit = x[1]

    try:
        num = float(num)
        print(num)
    except:
        raise exception

    if unit in ('bits', 'bit'):
        unit = 'b'
    elif unit in ('byte', 'bytes'):
        unit = 'B'
    else:
        unit = unit.lower()



    # split_idx = -1
    # split_chr = ''
    # for c in str:
    #     if c.isdigitl

