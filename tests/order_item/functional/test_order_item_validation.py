from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.test import TestCase

from order.models import Order
from order_item.models import OrderItem


class OrderItemValidationTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            customer_name="John Doe", customer_doc="12345678901"
        )

    def test_blank_product_url_is_rejected(self):
        item = OrderItem(
            order=self.order,
            product_code=uuid4(),
            product_name="Vinyl",
            product_url="",
            product_quantity=1,
        )
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("product_url", context.exception.message_dict)

    def test_blank_product_name_is_rejected(self):
        item = OrderItem(
            order=self.order, product_code=uuid4(), product_name="", product_quantity=1
        )
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("product_name", context.exception.message_dict)

    def test_negative_product_quantity_is_rejected(self):
        item = OrderItem(
            order=self.order,
            product_code=uuid4(),
            product_name="Vinyl",
            product_quantity=-1,
        )
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("product_quantity", context.exception.message_dict)

    def test_product_price_and_line_price_precision_are_validated(self):
        item = OrderItem(
            order=self.order,
            product_code=uuid4(),
            product_name="Vinyl",
            product_price=Decimal("10.999"),
            product_quantity=1,
            price=Decimal("12345678901.00"),
        )
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("product_price", context.exception.message_dict)
        self.assertIn("price", context.exception.message_dict)

    def test_save_runs_model_validation(self):
        item = OrderItem(
            order=self.order, product_code=uuid4(), product_name="", product_quantity=1
        )
        with self.assertRaises(ValidationError):
            item.save()
