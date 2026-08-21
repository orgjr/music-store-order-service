from unittest.mock import patch
from uuid import uuid4

from django.db import DatabaseError
from rest_framework import status
from rest_framework.test import APITestCase

from order.models import Order
from order_item.models import OrderItem


class OrderListEndpointTests(APITestCase):
    def create_order(self, name="John Doe"):
        return Order.objects.create(customer_name=name, customer_doc="12345678901")

    def test_list_returns_paginated_orders_newest_first(self):
        older = self.create_order("Older")
        newer = self.create_order("Newer")

        response = self.client.get("/api/v1/order/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["uuid"], str(newer.uuid))
        self.assertEqual(response.data["results"][1]["uuid"], str(older.uuid))


class OrderCreateEndpointTests(APITestCase):
    payload = {
        "customer": "5e8b0c11-d2f3-4a5b-8c9d-1e2f3a4b5c6d",
        "cart": "1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
        "payment_type": "CC",
    }

    @patch("order.views.OrderService.process")
    def test_create_returns_processed_order(self, process):
        order = Order.objects.create(
            customer_id=self.payload["customer"],
            customer_name="John Doe",
            customer_doc="12345678901",
            payment_type=Order.PaymentType.CREDIT_CARD,
        )
        process.return_value = order

        response = self.client.post("/api/v1/order/", self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["uuid"], str(order.uuid))
        self.assertEqual(response.data["payment_type"], "Credit card")
        process.assert_called_once()

    def test_create_requires_checkout_references(self):
        response = self.client.post("/api/v1/order/", {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data), {"customer", "cart", "payment_type"})

    def test_create_rejects_invalid_uuid(self):
        response = self.client.post(
            "/api/v1/order/", {**self.payload, "cart": "invalid"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("cart", response.data)

    @patch("order.services.process.validate_item")
    @patch(
        "order.services.process.get_service_url", return_value="https://catalog.test"
    )
    @patch("order.services.process.request_cart")
    @patch("order.services.process.request_user")
    @patch("order.services.process.OrderItem.objects.create")
    def test_create_database_error_rolls_back_logs_and_returns_500(
        self,
        create_item,
        request_user,
        request_cart,
        get_service_url,
        validate_item,
    ):
        request_user.return_value = {
            "uuid": self.payload["customer"],
            "first_name": "John",
            "last_name": "Doe",
            "doc": "12345678901",
        }
        request_cart.return_value = {
            "price": "49.90",
            "items": [
                {
                    "product_id": str(uuid4()),
                    "product_name": "Vinyl",
                    "product_slug": "vinyl",
                    "product_price": "49.90",
                    "quantity": 1,
                    "price": "49.90",
                }
            ],
        }
        create_item.side_effect = DatabaseError("database unavailable")

        with self.assertLogs("order.views", level="ERROR") as logs:
            response = self.client.post("/api/v1/order/", self.payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"order": "Order could not be processed"})
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)
        self.assertIn("Order processing failed.", logs.output[0])


class OrderRetrieveAndDestroyEndpointTests(APITestCase):
    def setUp(self):
        self.order = Order.objects.create(
            customer_name="John Doe", customer_doc="12345678901"
        )

    def test_retrieve_returns_order(self):
        response = self.client.get(f"/api/v1/order/{self.order.uuid}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(self.order.uuid))
        self.assertIn("customer_doc", response.data)
        self.assertIn("updated_at", response.data)

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get(f"/api/v1/order/{uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_removes_order_and_its_items(self):
        OrderItem.objects.create(
            order=self.order,
            product_code=uuid4(),
            product_name="Vinyl",
            product_url="https://catalog.test/vinyl",
            product_quantity=1,
        )

        response = self.client.delete(f"/api/v1/order/{self.order.uuid}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(uuid=self.order.uuid).exists())
        self.assertEqual(OrderItem.objects.count(), 0)
