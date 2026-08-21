from decimal import Decimal
from uuid import UUID, uuid4

from django.db import models


class Order(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    customer_id = models.UUIDField(default=uuid4, editable=False)
    customer_name = models.CharField(max_length=100)
    customer_email = models.CharField(max_length=100, null=True, blank=True)
    customer_doc = models.CharField(max_length=11)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    class PaymentType(models.TextChoices):
        PAYMENT_SLIP = "PS", "Payment slip"
        CREDIT_CARD = "CC", "Credit card"

    payment_type = models.CharField(
        max_length=2, choices=PaymentType.choices, default=PaymentType.PAYMENT_SLIP
    )

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELED = "CANCELED", "Canceled"

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"order: {self.uuid}, customer: {self.customer_email}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if not isinstance(self.uuid, UUID):
            self.uuid = uuid4()
