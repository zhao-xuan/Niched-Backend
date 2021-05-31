import unittest

from niched.example2 import dec


class Example2TestCase(unittest.TestCase):
    def test_dec(self):
        self.assertEqual(0, dec(1))
