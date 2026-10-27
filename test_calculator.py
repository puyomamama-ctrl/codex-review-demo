import unittest

from calculator import add


class AddTests(unittest.TestCase):
    def test_positive_integers(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative_integers(self):
        self.assertEqual(add(-2, -3), -5)

    def test_mixed_signs(self):
        self.assertEqual(add(-2, 3), 1)

    def test_zero(self):
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(0, 7), 7)
        self.assertEqual(add(7, 0), 7)


if __name__ == "__main__":
    unittest.main()
