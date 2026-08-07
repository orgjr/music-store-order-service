from decimal import Decimal
from typing import ClassVar
from uuid import uuid4

from django.db import models

from order.models import Order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_code = models.UUIDField(default=uuid4, editable=False, unique=True)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField(blank=True, null=True)
    product_quantity = models.PositiveSmallIntegerField()
    item_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    class Meta:
        ordering: ClassVar = ["product_name"]
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["product_code", "order"], name="one_product_per_order"
            )
        ]
