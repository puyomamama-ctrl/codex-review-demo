import unittest

from shipping import shipping_fee


class ShippingTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(shipping_fee(0), 500)

    def test_below_threshold(self):
        self.assertEqual(shipping_fee(4999), 500)

    def test_at_threshold(self):
        self.assertEqual(shipping_fee(5000), 0)

    def test_above_threshold(self):
        self.assertEqual(shipping_fee(5001), 0)

    def test_negative_total(self):
        with self.assertRaises(ValueError):
            shipping_fee(-1)


if __name__ == "__main__":
    unittest.main()
