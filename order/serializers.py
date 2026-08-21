from rest_framework import serializers

from order.models import Order
from order_item.models import OrderItem


class OrderRequestSerializer(serializers.Serializer):
    customer = serializers.UUIDField()
    cart = serializers.UUIDField()
    payment_type = serializers.CharField(
        max_length=2
    )  # PS=Payment slip or CC=Credit card


class OrderItemResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderResponseSerializer(serializers.ModelSerializer):
    items = OrderItemResponseSerializer(many=True, read_only=True)
    payment_type = serializers.CharField(
        source="get_payment_type_display", read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"
