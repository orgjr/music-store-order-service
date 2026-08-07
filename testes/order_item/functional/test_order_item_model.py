from decimal import Decimal
from uuid import UUID

from django.db import IntegrityError
from django.test import TestCase

from order.models import Order
from order_item.models import OrderItem


class OrderItemModelTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(customer_name="John Doe")

    def test_order_item_is_created_with_defaults(self):
        item = OrderItem.objects.create(
            order=self.order,
            product_name="Vinyl",
            product_quantity=2,
        )
        self.assertEqual(item.item_price, Decimal("0.00"))
        self.assertIsNone(item.product_description)
        self.assertIsInstance(item.product_code, UUID)

    def test_order_item_is_created_with_custom_values(self):
        item = OrderItem.objects.create(
            order=self.order,
            product_code=UUID("12345678-1234-5678-1234-567812345678"),
            product_name="Vinyl",
            product_description="Limited edition",
            product_quantity=3,
            item_price=Decimal("49.90"),
        )
        self.assertEqual(item.product_code, UUID("12345678-1234-5678-1234-567812345678"))
        self.assertEqual(item.product_description, "Limited edition")
        self.assertEqual(item.product_quantity, 3)
        self.assertEqual(item.item_price, Decimal("49.90"))

    def test_order_items_are_related_to_order(self):
        OrderItem.objects.create(order=self.order, product_name="Vinyl", product_quantity=1)
        OrderItem.objects.create(order=self.order, product_name="CD", product_quantity=1)
        self.assertEqual(self.order.items.count(), 2)

    def test_order_items_are_ordered_by_product_name(self):
        OrderItem.objects.create(order=self.order, product_name="Vinyl", product_quantity=1)
        OrderItem.objects.create(order=self.order, product_name="CD", product_quantity=1)
        names = list(self.order.items.values_list("product_name", flat=True))
        self.assertEqual(names, ["CD", "Vinyl"])

    def test_unique_product_per_order(self):
        product_code = UUID("12345678-1234-5678-1234-567812345678")
        OrderItem.objects.create(
            order=self.order,
            product_code=product_code,
            product_name="Vinyl",
            product_quantity=1,
        )
        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(
                order=self.order,
                product_code=product_code,
                product_name="Vinyl",
                product_quantity=1,
            )

    def test_product_code_is_unique_globally(self):
        product_code = UUID("12345678-1234-5678-1234-567812345678")
        other_order = Order.objects.create(customer_name="Jane Doe")
        OrderItem.objects.create(
            order=self.order,
            product_code=product_code,
            product_name="Vinyl",
            product_quantity=1,
        )
        with self.assertRaises(IntegrityError):
            OrderItem.objects.create(
                order=other_order,
                product_code=product_code,
                product_name="Vinyl",
                product_quantity=1,
            )

    def test_distinct_product_codes_allowed_on_different_orders(self):
        other_order = Order.objects.create(customer_name="Jane Doe")
        OrderItem.objects.create(order=self.order, product_name="Vinyl", product_quantity=1)
        OrderItem.objects.create(order=other_order, product_name="CD", product_quantity=1)
        self.assertEqual(OrderItem.objects.count(), 2)

    def test_deleting_order_cascades_to_items(self):
        OrderItem.objects.create(order=self.order, product_name="Vinyl", product_quantity=1)
        self.order.delete()
        self.assertEqual(OrderItem.objects.count(), 0)
