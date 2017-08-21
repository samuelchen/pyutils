#!/usr/bin/env python
# coding: utf-8

"""
Singly/doubly link and node
ref: https://stackoverflow.com/questions/280243/python-linked-list
"""
import weakref


class LinkNode(object):

    def __init__(self, cargo=None, next=None):
        self._cargo = cargo
        self._next = next

    @property
    def cargo(self):
        return self._cargo()

    @cargo.setter
    def cargo(self, value):
        self._cargo = weakref.ref(value)

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        assert isinstance(node, LinkNode)
        self._next = node
