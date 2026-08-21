from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from validators.price import validate_product_price
from validators.stock import validate_stock


class CatalogValidationTests(SimpleTestCase):
    item = {"product_name": "Vinyl", "product_price": "29.95", "quantity": 2}

    def test_price_validation_accepts_matching_price(self):
        self.assertTrue(validate_product_price({"price": "29.95"}, self.item))

    def test_price_validation_rejects_inconsistent_price(self):
        with self.assertRaisesMessage(ValidationError, "inconsistent price"):
            validate_product_price({"price": "30.00"}, self.item)

    def test_stock_validation_accepts_available_stock(self):
        self.assertTrue(validate_stock({"stock": 2}, self.item))

    def test_stock_validation_rejects_insufficient_stock(self):
        with self.assertRaisesMessage(ValidationError, "no stock available"):
            validate_stock({"stock": 1}, self.item)
