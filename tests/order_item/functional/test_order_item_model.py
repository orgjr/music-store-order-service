from decimal import Decimal
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError
from django.test import TestCase

from order.models import Order
from order_item.models import OrderItem


class OrderItemModelTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            customer_name="John Doe", customer_doc="12345678901"
        )

    def test_order_item_persists_catalog_snapshot(self):
        product_code = uuid4()
        item = OrderItem.objects.create(
            order=self.order,
            product_code=product_code,
            product_name="Vinyl",
            product_url="https://catalog.test/vinyl",
            product_price=Decimal("29.95"),
            product_quantity=2,
            price=Decimal("59.90"),
        )

        self.assertIsInstance(item.uuid, UUID)
        self.assertEqual(item.product_code, product_code)
        self.assertEqual(item.product_price, Decimal("29.95"))
        self.assertEqual(item.price, Decimal("59.90"))

    def test_order_items_are_ordered_by_product_name(self):
        OrderItem.objects.create(
            order=self.order,
            product_code=uuid4(),
            product_name="Vinyl",
            product_url="https://catalog.test/vinyl",
            product_quantity=1,
        )
        OrderItem.objects.create(
            order=self.order,
            product_code=uuid4(),
            product_name="CD",
            product_url="https://catalog.test/cd",
            product_quantity=1,
        )

        names = list(self.order.items.values_list("product_name", flat=True))
        self.assertEqual(names, ["CD", "Vinyl"])

    def test_product_code_must_be_unique_per_order(self):
        product_code = uuid4()
        OrderItem.objects.create(
            order=self.order,
            product_code=product_code,
            product_name="Vinyl",
            product_url="https://catalog.test/vinyl",
            product_quantity=1,
        )

        with self.assertRaises(ValidationError) as context:
            OrderItem.objects.create(
                order=self.order,
                product_code=product_code,
                product_name="Vinyl",
                product_url="https://catalog.test/vinyl",
                product_quantity=1,
            )

        self.assertIn("__all__", context.exception.message_dict)

    def test_same_product_code_is_allowed_on_another_order(self):
        product_code = uuid4()
        other_order = Order.objects.create(
            customer_name="Jane Doe", customer_doc="98765432100"
        )
        OrderItem.objects.create(
            order=self.order,
            product_code=product_code,
            product_name="Vinyl",
            product_url="https://catalog.test/vinyl",
            product_quantity=1,
        )
        OrderItem.objects.create(
            order=other_order,
            product_code=product_code,
            product_name="Vinyl",
            product_url="https://catalog.test/vinyl",
            product_quantity=1,
        )

        self.assertEqual(OrderItem.objects.count(), 2)
