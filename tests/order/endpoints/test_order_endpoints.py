from decimal import Decimal
from uuid import uuid4

from rest_framework import status
from rest_framework.test import APITestCase

from order.models import Order


class OrderListEndpointTests(APITestCase):
    def test_list_returns_200(self):
        response = self.client.get("/api/v1/order/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_is_paginated(self):
        Order.objects.create(customer_name="John Doe")
        response = self.client.get("/api/v1/order/")
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 1)

    def test_list_orders_newest_first(self):
        older = Order.objects.create(customer_name="Older")
        newer = Order.objects.create(customer_name="Newer")
        response = self.client.get("/api/v1/order/")
        results = response.data["results"]
        self.assertEqual(results[0]["uuid"], str(newer.uuid))
        self.assertEqual(results[1]["uuid"], str(older.uuid))

    def test_list_method_not_allowed(self):
        response = self.client.put("/api/v1/order/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class OrderCreateEndpointTests(APITestCase):
    def test_create_returns_201(self):
        response = self.client.post(
            "/api/v1/order/",
            {"customer_name": "John Doe", "price": "129.90"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_persists_order(self):
        response = self.client.post(
            "/api/v1/order/",
            {"customer_name": "John Doe", "payment_type": "CC"},
            format="json",
        )
        order = Order.objects.get(uuid=response.data["uuid"])
        self.assertEqual(order.customer_name, "John Doe")
        self.assertEqual(order.payment_type, Order.PaymentType.CREDIT_CARD)
        self.assertEqual(order.price, Decimal("0.00"))
        self.assertEqual(order.status, Order.Status.PENDING)

    def test_create_assigns_auto_uuid(self):
        response = self.client.post(
            "/api/v1/order/", {"customer_name": "John Doe"}, format="json"
        )
        self.assertIn("uuid", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("customer_id", response.data)

    def test_create_without_customer_name_returns_400(self):
        response = self.client.post("/api/v1/order/", {"price": "10.00"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("customer_name", response.data)

    def test_create_with_invalid_payment_type_returns_400(self):
        response = self.client.post(
            "/api/v1/order/",
            {"customer_name": "John Doe", "payment_type": "XX"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("payment_type", response.data)


class OrderRetrieveEndpointTests(APITestCase):
    def test_retrieve_returns_200(self):
        order = Order.objects.create(customer_name="John Doe")
        response = self.client.get(f"/api/v1/order/{order.uuid}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uuid"], str(order.uuid))

    def test_retrieve_nonexistent_returns_404(self):
        response = self.client.get(f"/api/v1/order/{uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_invalid_uuid_returns_404(self):
        response = self.client.get("/api/v1/order/not-a-uuid/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderUpdateEndpointTests(APITestCase):
    def test_partial_update_returns_200(self):
        order = Order.objects.create(customer_name="John Doe")
        response = self.client.patch(
            f"/api/v1/order/{order.uuid}/", {"status": "PAID"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID)

    def test_full_update_returns_200(self):
        order = Order.objects.create(customer_name="John Doe")
        response = self.client.put(
            f"/api/v1/order/{order.uuid}/",
            {"customer_name": "Jane Doe", "price": "50.00"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.customer_name, "Jane Doe")
        self.assertEqual(order.price, Decimal("50.00"))

    def test_partial_update_nonexistent_returns_404(self):
        response = self.client.patch(
            f"/api/v1/order/{uuid4()}/", {"status": "PAID"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderDestroyEndpointTests(APITestCase):
    def test_destroy_returns_204(self):
        order = Order.objects.create(customer_name="John Doe")
        response = self.client.delete(f"/api/v1/order/{order.uuid}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_deletes_order(self):
        order = Order.objects.create(customer_name="John Doe")
        self.client.delete(f"/api/v1/order/{order.uuid}/")
        self.assertFalse(Order.objects.filter(uuid=order.uuid).exists())

    def test_destroy_nonexistent_returns_404(self):
        response = self.client.delete(f"/api/v1/order/{uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
