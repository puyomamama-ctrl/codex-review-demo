import unittest

from discount import discounted_price


class DiscountTests(unittest.TestCase):
    def test_zero_discount(self):
        self.assertEqual(discounted_price(1000, 0), 1000)

    def test_negative_discount_raises(self):
        with self.assertRaises(ValueError):
            discounted_price(1000, -1)

    def test_discount_above_one_hundred_raises(self):
        with self.assertRaises(ValueError):
            discounted_price(1000, 101)

    def test_ten_percent_discount(self):
        self.assertEqual(discounted_price(1000, 10), 900)

    def test_half_price(self):
        self.assertEqual(discounted_price(1000, 50), 500)

    def test_full_discount(self):
        self.assertEqual(discounted_price(1000, 100), 0)

    def test_fractional_price_rounds_down(self):
        self.assertEqual(discounted_price(999, 10), 899)


if __name__ == "__main__":
    unittest.main()
