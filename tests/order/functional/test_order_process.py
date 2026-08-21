from unittest.mock import patch
from uuid import UUID, uuid4

from django.test import TestCase

from order.models import Order
from order.services.process import OrderService
from order_item.models import OrderItem


class OrderProcessTests(TestCase):
    customer_id = uuid4()
    cart_id = uuid4()

    @patch("order.services.process.validate_item")
    @patch(
        "order.services.process.get_service_url", return_value="https://catalog.test"
    )
    @patch("order.services.process.request_cart")
    @patch("order.services.process.request_user")
    def test_process_persists_order_and_catalog_snapshot(
        self, request_user, request_cart, get_service_url, validate_item
    ):
        request_user.return_value = {
            "uuid": str(self.customer_id),
            "first_name": "John",
            "last_name": "Doe",
            "doc": "12345678901",
        }
        item = {
            "product_id": str(uuid4()),
            "product_name": "Vinyl",
            "product_slug": "vinyl",
            "product_price": "29.95",
            "quantity": 2,
            "price": "59.90",
        }
        request_cart.return_value = {"price": "59.90", "items": [item]}

        order = OrderService.process(self.customer_id, self.cart_id, "PS")

        self.assertEqual(order.customer_id, self.customer_id)
        self.assertEqual(order.customer_name, "John Doe")
        self.assertEqual(str(order.price), "59.90")
        snapshot = order.items.get()
        self.assertIsInstance(snapshot.uuid, UUID)
        self.assertEqual(snapshot.product_url, "https://catalog.test/vinyl")
        self.assertEqual(str(snapshot.product_price), "29.95")
        validate_item.assert_called_once_with(item)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
