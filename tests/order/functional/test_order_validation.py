from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from order.models import Order


class OrderValidationTests(TestCase):
    customer_doc = "12345678901"

    def test_invalid_payment_type_is_rejected(self):
        order = Order(
            customer_name="John Doe", customer_doc=self.customer_doc, payment_type="XX"
        )
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertIn("payment_type", context.exception.message_dict)

    def test_invalid_status_is_rejected(self):
        order = Order(
            customer_name="John Doe", customer_doc=self.customer_doc, status="NOPE"
        )
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertIn("status", context.exception.message_dict)

    def test_blank_customer_name_is_rejected(self):
        order = Order(customer_name="", customer_doc=self.customer_doc)
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertIn("customer_name", context.exception.message_dict)

    def test_missing_customer_name_is_rejected(self):
        order = Order(customer_doc=self.customer_doc)
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertIn("customer_name", context.exception.message_dict)

    def test_price_decimal_places_are_validated(self):
        order = Order(
            customer_name="John Doe",
            customer_doc=self.customer_doc,
            price=Decimal("99.999"),
        )
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertIn("price", context.exception.message_dict)

    def test_price_max_digits_are_validated(self):
        order = Order(
            customer_name="John Doe",
            customer_doc=self.customer_doc,
            price=Decimal("12345678901.00"),
        )
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertIn("price", context.exception.message_dict)

    def test_negative_price_is_allowed(self):
        order = Order(
            customer_name="John Doe",
            customer_doc=self.customer_doc,
            price=Decimal("-10.00"),
        )
        order.full_clean()
        order.save()
        self.assertEqual(order.price, Decimal("-10.00"))

    def test_customer_name_longer_than_max_length_is_rejected(self):
        order = Order(customer_name="x" * 101, customer_doc=self.customer_doc)
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertIn("customer_name", context.exception.message_dict)

    def test_save_runs_full_clean_and_raises(self):
        order = Order(customer_name="", customer_doc=self.customer_doc)
        with self.assertRaises(ValidationError):
            order.save()

    def test_valid_order_passes_full_clean(self):
        order = Order(customer_name="John Doe", customer_doc=self.customer_doc)
        order.full_clean()
        self.assertEqual(order.uuid is not None, True)

    def test_missing_customer_doc_is_rejected(self):
        order = Order(customer_name="John Doe")
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertIn("customer_doc", context.exception.message_dict)

    def test_customer_doc_longer_than_max_length_is_rejected(self):
        order = Order(customer_name="John Doe", customer_doc="1" * 12)
        with self.assertRaises(ValidationError) as context:
            order.full_clean()
        self.assertIn("customer_doc", context.exception.message_dict)
