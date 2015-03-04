#!/usr/bin/env python
# coding: utf-8
__author__ = 'Samuel Chen <samuel.net@gmail.com>'

'''
strings module description

Created on 3/3/2015
'''

import hashlib

def hash(str, len=0, coder='md5'):
    '''
    Encoding given string (str) by encoder (coder), return first "len" chars.
    :param str: String to be encoded
    :param len: Return length. If len is 0, return whole encoded string.
    :param coder: The encoder. Support 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'
    :return: Encoded string.
    '''
    hashlib.algorithms
    encoder = getattr(hashlib, coder)
    if not encoder:
        encoder = hashlib.md5
    v = encoder(str).hexdigest()
    if 0 == len:
        return v
    else:
        return v[:len]

def md5(str, len=0):
    '''
    Encoding given string (str) in MD5, return first "len" chars.
    :param str: String to be encoded
    :param len: Return length. If len is 0, return whole encoded string.
    :return: Encoded string.
    '''
    return hash(str, len, coder='md5')

def sha1(str, len=0):
    '''
    Encoding given string (str) in SHA1, return first "len" chars.
    :param str: String to be encoded
    :param len: Return length. If len is 0, return whole encoded string.
    :return: Encoded string.
    '''
    return hash(str, len, coder='sha1')

def sha256(str, len=0):
    '''
    Encoding given string (str) in SHA256, return first "len" chars.
    :param str: String to be encoded
    :param len: Return length. If len is 0, return whole encoded string.
    :return: Encoded string.
    '''
    return hash(str, len, coder='sha256')