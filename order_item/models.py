from decimal import Decimal
from typing import ClassVar
from uuid import UUID, uuid4

from django.db import models

from order.models import Order


class OrderItem(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_code = models.UUIDField(editable=False)
    product_name = models.CharField(max_length=100)
    product_url = models.CharField(max_length=300, null=True)
    product_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    product_quantity = models.PositiveSmallIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    class Meta:
        ordering: ClassVar = ["product_name"]
        constraints: ClassVar = [
            models.UniqueConstraint(
                fields=["product_code", "order"], name="one_product_per_order"
            )
        ]

    def __str__(self):
        return f"{self.product_name}, quantity: {self.product_quantity}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if not isinstance(self.uuid, UUID):
            self.uuid = uuid4()
