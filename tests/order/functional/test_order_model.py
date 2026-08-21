from decimal import Decimal
from uuid import UUID

from django.test import TestCase

from order.models import Order


class OrderModelTests(TestCase):
    customer_doc = "12345678901"

    def test_order_is_created_with_defaults(self):
        order = Order.objects.create(
            customer_name="John Doe", customer_doc=self.customer_doc
        )
        self.assertEqual(order.status, Order.Status.PENDING)
        self.assertEqual(order.payment_type, Order.PaymentType.PAYMENT_SLIP)
        self.assertEqual(order.price, Decimal("0.00"))

    def test_order_gets_auto_uuid_and_created_at(self):
        order = Order.objects.create(
            customer_name="John Doe", customer_doc=self.customer_doc
        )
        self.assertIsInstance(order.uuid, UUID)
        self.assertIsNotNone(order.created_at)
        self.assertIsNotNone(order.updated_at)

    def test_order_is_created_with_custom_values(self):
        order = Order.objects.create(
            customer_id=UUID("12345678-1234-5678-1234-567812345678"),
            customer_name="John Doe",
            customer_email="john@example.com",
            customer_doc=self.customer_doc,
            price=Decimal("99.90"),
            payment_type=Order.PaymentType.CREDIT_CARD,
            status=Order.Status.PAID,
        )
        self.assertEqual(
            order.customer_id, UUID("12345678-1234-5678-1234-567812345678")
        )
        self.assertEqual(order.price, Decimal("99.90"))
        self.assertEqual(order.payment_type, Order.PaymentType.CREDIT_CARD)
        self.assertEqual(order.status, Order.Status.PAID)
        self.assertEqual(order.customer_email, "john@example.com")

    def test_order_payment_type_choices(self):
        for choice in Order.PaymentType.values:
            order = Order.objects.create(
                customer_name="John Doe",
                customer_doc=self.customer_doc,
                payment_type=choice,
            )
            self.assertEqual(order.payment_type, choice)

    def test_order_status_choices(self):
        for choice in Order.Status.values:
            order = Order.objects.create(
                customer_name="John Doe", customer_doc=self.customer_doc, status=choice
            )
            self.assertEqual(order.status, choice)

    def test_order_customer_name_max_length(self):
        field = Order._meta.get_field("customer_name")
        self.assertEqual(field.max_length, 100)

    def test_order_string_representation_uses_customer_email(self):
        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            customer_doc=self.customer_doc,
        )
        self.assertIn("john@example.com", str(order))
