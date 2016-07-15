__author__ = 'samuel'

import unittest
from ..converter import storage_size_to_byte


class TestConverter(unittest.TestCase):
    def test_storage_size_to_byte(self):
        bit = 1 / 8
        B = 8 * bit
        KB = 1024 * B
        MB = 1024 * KB
        GB = 1024 * MB
        TB = 1024 * GB
        PB = 1024 * TB

        sizes = [
            ("24.5 TB", 24.5 * TB),
            ("83b", 83 * bit),
            ("38 B", 38 * B),
            ("343K", 343 * KB),
            ("18k", 18 * KB),
            ("93.5KB", 93.3 * KB),
            ("32 KB", 32 * KB),
            ("38.5 k", 38.5 * KB),
            ("25MB", 25 * MB),
            ("38.5 M", 38.5 * MB),
            ("28 gb", 28 * GB),
            ("338 gB", 338 * GB),
            ("93 t", 93 * TB),
            ("17.5 P", 17.5 * PB),
        ]
        error_sizes = [
            '18.3KB',
            '23bit',
            '38byte',
            '3.3.3 GB',
            # '.33 M',
            '-34M',
            '-23 g',
            '-34.5K',
        ]

        for s, b in sizes:
            self.assertEqual(storage_size_to_byte(s), b)

        for s in error_sizes:
            with self.assertRaises(Exception):
                storage_size_to_byte(s)


if __name__ == '__main__':
    unittest.main()
