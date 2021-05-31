import unittest

from niched.example import inc


class ExampleTestCase(unittest.TestCase):
    def test_inc(self):
        self.assertEqual(1, inc(0))
