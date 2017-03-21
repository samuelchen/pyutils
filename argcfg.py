#!/usr/bin/env python
# coding: utf-8

"""
Arguments and Configs
"""

import argparse
import configparser
from pyutils.langutil import MutableEnum


class ArgCfg(object):

    def __init__(self):
        self._cfg_file = 'config.ini'
        self._arg_parser = argparse.ArgumentParser()
        self._cfg_parser = configparser.ConfigParser()
        self._arg_parser.add_argument('--config-file', '-f', dest='config_file', action='store',
                                      type=str, default='config.ini',
                                      help='load specified config file')

    def add_argument(self, *args, **kwargs):
        self._arg_parser.add_argument(*args, **kwargs)

    def set_config_file(self, cfg_file):
        self._cfg_file = cfg_file

    def parse(self):
        options = MutableEnum()

        args = self._arg_parser.parse_args()

        for k, v in vars(args).items():
            options[k] = v

        if args.config_file:
            self._cfg_file = args.config_file

        read_ok_list = self._cfg_parser.read(self._cfg_file)
        if self._cfg_file in read_ok_list:
            for section in self._cfg_parser.sections():
                sec = MutableEnum()
                for k, v in self._cfg_parser.items(section):
                    sec[k] = v
                options[section] = sec
        else:
            raise IOError('Fail to access %s' % self._cfg_file)
        return options

# global configs
cfgs = None
if cfgs is None:
    argcfg = ArgCfg()
    cfgs = argcfg.parse()

__all__ = [
    ArgCfg,
    cfgs,
]


if __name__ == '__main__':
    for k, v in cfgs:
        if isinstance(v, str):
            print(k, '=', v)
        else:
            print('[%s]' % k)
            for i, j in v:
                print('\t', i, '=', j)
