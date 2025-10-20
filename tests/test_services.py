import unittest
from unittest.mock import MagicMock, patch
from myshop.products import Product
from myshop.services import ProductService, ProductNotFoundError

class TestProductService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p1 = Product(1, "Mouse", 50.0)
        cls.p2 = Product(2, "Monitor", 100.0)

    def setUp(self):
        # novo mock a cada teste (isola dependências externas)
        self.repo = MagicMock()
        self.svc = ProductService(self.repo, tax_rate=0.10)  # 12,3% p/ evidenciar o bug

    def test_get_product_success_calls_repo(self):
        self.repo.get_by_id.return_value = self.p1
        prod = self.svc.get_product(1)
        self.assertEqual(prod, self.p1)
        self.repo.get_by_id.assert_called_once_with(1)

    def test_get_product_not_found(self):
        self.repo.get_by_id.side_effect = KeyError(99)
        with self.assertRaises(ProductNotFoundError):
            self.svc.get_product(99)

    def test_set_price_saves_updated(self):
        self.repo.get_by_id.return_value = self.p1
        self.svc.set_price(1, 60.0)
        saved = self.repo.save.call_args[0][0]
        self.assertEqual(saved.price, 60.0)

    def test_final_price_parametrized_with_subTest(self):
        self.repo.get_by_id.return_value = self.p2  # 100.0
        cases = [
            (0.10, True, 99.0),   # 100 -> 90 -> +10% = 99.0 (CORRETO)
            (0.00, True, 110.0),  # 100 -> +10% = 110.0
            (0.25, False, 75.0),  # sem imposto
        ]
        for discount, include_tax, expected in cases:
            with self.subTest(discount=discount, include_tax=include_tax):
                got = self.svc.final_price(2, discount=discount, include_tax=include_tax)
                self.assertEqual(got, expected)

    def test_final_price_rejects_invalid_discount(self):
        self.repo.get_by_id.return_value = self.p1
        for bad in (-0.1, 1.1):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    self.svc.final_price(1, discount=bad)
