import unittest

from clamp import clamp


class ClampTests(unittest.TestCase):
    def test_inside(self):
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_below(self):
        self.assertEqual(clamp(-5, 0, 10), 0)

    def test_above(self):
        self.assertEqual(clamp(20, 0, 10), 10)

    def test_lower_boundary(self):
        self.assertEqual(clamp(-10, -10, -1), -10)

    def test_upper_boundary(self):
        self.assertEqual(clamp(-1, -10, -1), -1)

    def test_equal_bounds(self):
        self.assertEqual(clamp(100, 0, 0), 0)

    def test_reversed_bounds(self):
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)


if __name__ == "__main__":
    unittest.main()
