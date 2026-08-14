from decimal import Decimal
from uuid import UUID

from django.test import TestCase

from order.models import Order
from order.serializers import OrderSerializer


class OrderSerializerTests(TestCase):
    def test_serializer_exposes_expected_fields(self):
        order = Order.objects.create(customer_name="John Doe")
        data = OrderSerializer(order).data
        expected_fields = {
            "uuid",
            "customer_id",
            "customer_name",
            "price",
            "payment_type",
            "status",
            "created_at",
            "items",
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_serializer_serializes_default_values(self):
        order = Order.objects.create(customer_name="John Doe")
        data = OrderSerializer(order).data
        self.assertEqual(data["customer_name"], "John Doe")
        self.assertEqual(data["price"], "0.00")
        self.assertEqual(data["payment_type"], Order.PaymentType.PAYMENT_SLIP)
        self.assertEqual(data["status"], Order.Status.PENDING)
        self.assertEqual(data["items"], [])

    def test_serializer_read_only_fields_are_present(self):
        order = Order.objects.create(customer_name="John Doe")
        data = OrderSerializer(order).data
        self.assertEqual(UUID(data["uuid"]), order.uuid)
        self.assertIsNotNone(data["created_at"])

    def test_serializer_is_valid_with_only_customer_name(self):
        serializer = OrderSerializer(data={"customer_name": "John Doe"})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.customer_name, "John Doe")

    def test_serializer_is_valid_with_custom_values(self):
        serializer = OrderSerializer(
            data={
                "customer_name": "John Doe",
                "price": "99.90",
                "payment_type": Order.PaymentType.CREDIT_CARD,
                "status": Order.Status.PAID,
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.price, Decimal("99.90"))
        self.assertEqual(order.payment_type, Order.PaymentType.CREDIT_CARD)
        self.assertEqual(order.status, Order.Status.PAID)

    def test_serializer_customer_id_is_auto_generated(self):
        serializer = OrderSerializer(data={"customer_name": "John Doe"})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.customer_id, UUID(str(order.customer_id)))

    def test_serializer_rejects_blank_customer_name(self):
        serializer = OrderSerializer(data={"customer_name": ""})
        self.assertFalse(serializer.is_valid())
        self.assertIn("customer_name", serializer.errors)

    def test_serializer_rejects_invalid_payment_type(self):
        serializer = OrderSerializer(
            data={"customer_name": "John Doe", "payment_type": "XX"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("payment_type", serializer.errors)

    def test_serializer_does_not_accept_uuid_on_create(self):
        serializer = OrderSerializer(
            data={
                "customer_name": "John Doe",
                "uuid": "12345678-1234-5678-1234-567812345678",
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertNotEqual(order.uuid, UUID("12345678-1234-5678-1234-567812345678"))

    def test_serializer_nested_items_are_serialized(self):
        order = Order.objects.create(customer_name="John Doe")
        item = order.items.create(product_name="Vinyl", product_quantity=1)
        data = OrderSerializer(order).data
        self.assertEqual(len(data["items"]), 1)
        self.assertEqual(data["items"][0]["product_name"], "Vinyl")
        self.assertEqual(data["items"][0]["id"], item.id)
