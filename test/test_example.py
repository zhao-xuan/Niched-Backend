import unittest

from niched.example import inc


class MyTestCase(unittest.TestCase):
    def test_inc(self):
        self.assertEqual(1, inc(0))


if __name__ == '__main__':
    unittest.main()
