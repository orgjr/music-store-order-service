from typing import ClassVar

from rest_framework import serializers

from order_item.serializers import OrderItemSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields: ClassVar = "__all__"
        read_only_fields = ("uuid", "created_at")
