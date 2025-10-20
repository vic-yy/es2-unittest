import unittest
from myshop.products import Product

class TestProduct(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample = Product(1, "Keyboard", 100.0)

    def test_with_price_returns_new_instance(self):
        # Arrange / Act
        p2 = self.sample.with_price(120.0)
        # Assert
        self.assertEqual(self.sample.price, 100.0)
        self.assertEqual(p2.price, 120.0)
        self.assertNotEqual(id(self.sample), id(p2))

    def test_with_price_rejects_negative(self):
        with self.assertRaises(ValueError):
            self.sample.with_price(-1)
