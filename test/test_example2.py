import unittest

from niched.example2 import dec


class MyTestCase(unittest.TestCase):
    def test_dec(self):
        self.assertEqual(0, dec(1))


if __name__ == '__main__':
    unittest.main()
