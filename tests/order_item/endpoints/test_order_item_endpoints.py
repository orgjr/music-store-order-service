from decimal import Decimal
from uuid import uuid4

from rest_framework import status
from rest_framework.test import APITestCase

from order.models import Order
from order_item.models import OrderItem


class OrderItemListEndpointTests(APITestCase):
    def setUp(self):
        self.order = Order.objects.create(customer_name="John Doe")

    def test_list_returns_200(self):
        response = self.client.get("/api/v1/order-item/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_is_paginated(self):
        OrderItem.objects.create(
            order=self.order, product_name="Vinyl", product_quantity=1
        )
        response = self.client.get("/api/v1/order-item/")
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 1)

    def test_list_method_not_allowed(self):
        response = self.client.delete("/api/v1/order-item/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class OrderItemCreateEndpointTests(APITestCase):
    def setUp(self):
        self.order = Order.objects.create(customer_name="John Doe")

    def test_create_returns_201(self):
        response = self.client.post(
            "/api/v1/order-item/",
            {
                "order": str(self.order.uuid),
                "product_name": "Vinyl",
                "product_quantity": 2,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_persists_item(self):
        response = self.client.post(
            "/api/v1/order-item/",
            {
                "order": str(self.order.uuid),
                "product_name": "Vinyl",
                "product_quantity": 2,
                "item_price": "49.90",
            },
            format="json",
        )
        item = OrderItem.objects.get(id=response.data["id"])
        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product_name, "Vinyl")
        self.assertEqual(item.product_quantity, 2)
        self.assertEqual(item.item_price, Decimal("49.90"))

    def test_create_assigns_auto_product_code(self):
        response = self.client.post(
            "/api/v1/order-item/",
            {
                "order": str(self.order.uuid),
                "product_name": "Vinyl",
                "product_quantity": 1,
            },
            format="json",
        )
        self.assertIn("product_code", response.data)
        self.assertIn("id", response.data)

    def test_create_without_product_name_returns_400(self):
        response = self.client.post(
            "/api/v1/order-item/",
            {"order": str(self.order.uuid), "product_quantity": 1},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("product_name", response.data)

    def test_create_with_nonexistent_order_returns_400(self):
        response = self.client.post(
            "/api/v1/order-item/",
            {"order": str(uuid4()), "product_name": "Vinyl", "product_quantity": 1},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("order", response.data)

    def test_create_with_negative_quantity_returns_400(self):
        response = self.client.post(
            "/api/v1/order-item/",
            {
                "order": str(self.order.uuid),
                "product_name": "Vinyl",
                "product_quantity": -1,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("product_quantity", response.data)


class OrderItemRetrieveEndpointTests(APITestCase):
    def setUp(self):
        self.order = Order.objects.create(customer_name="John Doe")

    def test_retrieve_returns_200(self):
        item = OrderItem.objects.create(
            order=self.order, product_name="Vinyl", product_quantity=1
        )
        response = self.client.get(f"/api/v1/order-item/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], item.id)
        self.assertEqual(response.data["product_name"], "Vinyl")

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get("/api/v1/order-item/999999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderItemUpdateEndpointTests(APITestCase):
    def setUp(self):
        self.order = Order.objects.create(customer_name="John Doe")
        self.item = OrderItem.objects.create(
            order=self.order, product_name="Vinyl", product_quantity=1
        )

    def test_partial_update_returns_200(self):
        response = self.client.patch(
            f"/api/v1/order-item/{self.item.id}/",
            {"product_quantity": 5},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.product_quantity, 5)

    def test_full_update_returns_200(self):
        response = self.client.put(
            f"/api/v1/order-item/{self.item.id}/",
            {
                "order": str(self.order.uuid),
                "product_name": "CD",
                "product_quantity": 3,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.product_name, "CD")
        self.assertEqual(self.item.product_quantity, 3)

    def test_partial_update_nonexistent_returns_404(self):
        response = self.client.patch(
            "/api/v1/order-item/999999/", {"product_quantity": 5}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderItemDestroyEndpointTests(APITestCase):
    def setUp(self):
        self.order = Order.objects.create(customer_name="John Doe")

    def test_destroy_returns_204(self):
        item = OrderItem.objects.create(
            order=self.order, product_name="Vinyl", product_quantity=1
        )
        response = self.client.delete(f"/api/v1/order-item/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_deletes_item(self):
        item = OrderItem.objects.create(
            order=self.order, product_name="Vinyl", product_quantity=1
        )
        self.client.delete(f"/api/v1/order-item/{item.id}/")
        self.assertFalse(OrderItem.objects.filter(id=item.id).exists())

    def test_destroy_nonexistent_returns_404(self):
        response = self.client.delete("/api/v1/order-item/999999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
