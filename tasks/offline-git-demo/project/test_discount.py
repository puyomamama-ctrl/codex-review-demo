import unittest
from discount import add
class Tests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
