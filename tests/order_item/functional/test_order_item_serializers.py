from decimal import Decimal
from uuid import UUID

from django.test import TestCase

from order.models import Order
from order_item.models import OrderItem
from order_item.serializers import OrderItemSerializer


class OrderItemSerializerTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(customer_name="John Doe")

    def test_serializer_exposes_expected_fields(self):
        item = OrderItem.objects.create(
            order=self.order, product_name="Vinyl", product_quantity=1
        )
        data = OrderItemSerializer(item).data
        expected_fields = {
            "id",
            "order",
            "product_code",
            "product_name",
            "product_description",
            "product_quantity",
            "item_price",
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_serializer_serializes_default_values(self):
        item = OrderItem.objects.create(
            order=self.order, product_name="Vinyl", product_quantity=1
        )
        data = OrderItemSerializer(item).data
        self.assertEqual(data["product_name"], "Vinyl")
        self.assertEqual(data["product_quantity"], 1)
        self.assertEqual(data["item_price"], "0.00")
        self.assertIsNone(data["product_description"])
        self.assertEqual(UUID(data["product_code"]), item.product_code)

    def test_serializer_is_valid_with_required_fields(self):
        serializer = OrderItemSerializer(
            data={
                "order": str(self.order.uuid),
                "product_name": "Vinyl",
                "product_quantity": 2,
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        item = serializer.save()
        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product_name, "Vinyl")
        self.assertEqual(item.product_quantity, 2)

    def test_serializer_is_valid_with_custom_values(self):
        serializer = OrderItemSerializer(
            data={
                "order": str(self.order.uuid),
                "product_name": "Vinyl",
                "product_description": "Limited edition",
                "product_quantity": 3,
                "item_price": "49.90",
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        item = serializer.save()
        self.assertEqual(item.product_description, "Limited edition")
        self.assertEqual(item.item_price, Decimal("49.90"))

    def test_serializer_rejects_blank_product_name(self):
        serializer = OrderItemSerializer(
            data={
                "order": str(self.order.uuid),
                "product_name": "",
                "product_quantity": 1,
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("product_name", serializer.errors)

    def test_serializer_rejects_zero_quantity(self):
        serializer = OrderItemSerializer(
            data={
                "order": str(self.order.uuid),
                "product_name": "Vinyl",
                "product_quantity": -1,
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("product_quantity", serializer.errors)

    def test_serializer_does_not_accept_product_code_on_create(self):
        serializer = OrderItemSerializer(
            data={
                "order": str(self.order.uuid),
                "product_name": "Vinyl",
                "product_quantity": 1,
                "product_code": "12345678-1234-5678-1234-567812345678",
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        item = serializer.save()
        self.assertNotEqual(
            item.product_code, UUID("12345678-1234-5678-1234-567812345678")
        )
