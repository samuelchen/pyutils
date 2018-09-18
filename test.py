import sys
from termcolor import colored, cprint
from pyutils.logger import ColorFormatter

__author__ = 'Samuel Chen <samuel.net@gmail.com>'
__date__ = '2016/7/4 22:58'
__doc__ = """
some test codes
"""


def test_color_term():
    text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
    print(text)
    cprint('Hello, World!', 'green', 'on_red')

    print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
    print_red_on_cyan('Hello, World!')
    print_red_on_cyan('Hello, Universe!')

    for i in range(10):
        cprint(i, 'magenta', end=' ')

    cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)


def test_dict_dot_proerty():
    a = {
        "foo": "bar",
    }
    print(a.foo)


if __name__ == '__main__':
    test_dict_dot_proerty()