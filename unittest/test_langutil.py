__author__ = 'samuel'

import unittest
from ..langutil import Enum, MutableEnum


class TestEnhancement(unittest.TestCase):
    def test_enum(self):
        prop_str = 'First Property'
        prop_int = 'Int Property'
        props = {
            "foo": "bar",
            "str": prop_str,
            "int": prop_int,
        }
        enum = Enum(props)

        self.assertEqual(enum.foo, "bar")
        self.assertEqual(enum['str'], prop_str)
        self.assertEqual(getattr(enum, 'int'), prop_int)
        self.assertTrue('foo' in enum)
        self.assertEqual(len(enum), 3)
        for k, v in enum:
            self.assertEqual(enum[k], props[k])

    def test_mutableenum(self):
        prop_str = 'First Property'
        prop_int = 'Int Property'
        props = {
            "foo": "bar",
            "str": prop_str,
            "int": prop_int,
        }
        enum = MutableEnum(props)

        self.assertEqual(enum.foo, "bar")
        self.assertEqual(enum['str'], prop_str)
        self.assertEqual(getattr(enum, 'int'), prop_int)
        self.assertTrue('foo' in enum)
        self.assertEqual(len(enum), 3)
        for k, v in enum:
            self.assertEqual(enum[k], props[k])
        del enum['foo']
        self.assertTrue('foo' not in enum)
        self.assertEqual(len(enum), 2)
        x = enum.pop('str')
        self.assertEqual(x, prop_str)
        self.assertEqual(len(enum), 1)
        y = enum.popitem()
        self.assertEqual(y, prop_int)
        self.assertEqual(len(enum), 0)

        with self.assertRaises(AttributeError):
            enum.foo

        new_props = {
            "name": "Jack",
            "age": 18,
        }
        enum.update(new_props)
        self.assertEqual(len(enum), 2)
        self.assertEqual(enum.name, 'Jack')
        for k, v in enum:
            self.assertEqual(enum[k], new_props[k])


if __name__ == '__main__':
    unittest.main()
