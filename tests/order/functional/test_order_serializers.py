from uuid import UUID, uuid4

from django.test import TestCase

from order.models import Order
from order.serializers import OrderRequestSerializer, OrderResponseSerializer
from order_item.models import OrderItem


class OrderSerializerTests(TestCase):
    def test_checkout_request_accepts_valid_references(self):
        serializer = OrderRequestSerializer(
            data={"customer": str(uuid4()), "cart": str(uuid4()), "payment_type": "CC"}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["payment_type"], "CC")

    def test_checkout_request_requires_all_fields_and_valid_uuids(self):
        serializer = OrderRequestSerializer(data={"customer": "invalid"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("customer", serializer.errors)
        self.assertIn("cart", serializer.errors)
        self.assertIn("payment_type", serializer.errors)

    def test_order_response_serializes_customer_and_item_snapshots(self):
        order = Order.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            customer_doc="12345678901",
            payment_type=Order.PaymentType.CREDIT_CARD,
        )
        item = OrderItem.objects.create(
            order=order,
            product_code=uuid4(),
            product_name="Vinyl",
            product_url="https://catalog.test/vinyl",
            product_quantity=1,
        )
        data = OrderResponseSerializer(order).data

        self.assertEqual(data["customer_email"], "john@example.com")
        self.assertEqual(data["customer_doc"], "12345678901")
        self.assertEqual(data["payment_type"], "Credit card")
        self.assertIn("updated_at", data)
        self.assertEqual(UUID(data["items"][0]["uuid"]), item.uuid)
