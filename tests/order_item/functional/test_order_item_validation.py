from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from order.models import Order
from order_item.models import OrderItem


class OrderItemValidationTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(customer_name="John Doe")

    def test_blank_product_name_is_rejected(self):
        item = OrderItem(order=self.order, product_name="", product_quantity=1)
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("product_name", context.exception.message_dict)

    def test_missing_product_quantity_is_rejected(self):
        item = OrderItem(order=self.order, product_name="Vinyl")
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("product_quantity", context.exception.message_dict)

    def test_zero_product_quantity_is_allowed(self):
        item = OrderItem(order=self.order, product_name="Vinyl", product_quantity=0)
        item.full_clean()
        item.save()
        self.assertEqual(item.product_quantity, 0)

    def test_negative_product_quantity_is_rejected(self):
        item = OrderItem(order=self.order, product_name="Vinyl", product_quantity=-1)
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("product_quantity", context.exception.message_dict)

    def test_item_price_decimal_places_are_validated(self):
        item = OrderItem(
            order=self.order,
            product_name="Vinyl",
            product_quantity=1,
            item_price=Decimal("10.999"),
        )
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("item_price", context.exception.message_dict)

    def test_item_price_max_digits_are_validated(self):
        item = OrderItem(
            order=self.order,
            product_name="Vinyl",
            product_quantity=1,
            item_price=Decimal("12345678901.00"),
        )
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("item_price", context.exception.message_dict)

    def test_product_name_longer_than_max_length_is_rejected(self):
        item = OrderItem(order=self.order, product_name="x" * 101, product_quantity=1)
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("product_name", context.exception.message_dict)

    def test_missing_order_is_rejected(self):
        item = OrderItem(product_name="Vinyl", product_quantity=1)
        with self.assertRaises(ValidationError) as context:
            item.full_clean()
        self.assertIn("order", context.exception.message_dict)

    def test_valid_item_passes_full_clean(self):
        item = OrderItem(order=self.order, product_name="Vinyl", product_quantity=1)
        item.full_clean()
        item.save()
        self.assertEqual(OrderItem.objects.count(), 1)
