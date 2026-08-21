import logging

from django.core.exceptions import ValidationError
from django.db import DatabaseError, Error
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from docs.openapi import order_schema
from order.services.process import OrderService

from .models import Order
from .serializers import OrderRequestSerializer, OrderResponseSerializer

logger = logging.getLogger(__name__)


@order_schema
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderResponseSerializer
        return OrderRequestSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            order = OrderService.process(
                customer=data["customer"],
                cart=data["cart"],
                payment_type=data["payment_type"],
            )
        except (Error, DatabaseError, ValidationError, Order.DoesNotExist):
            logger.exception("Order processing failed.")
            return Response(
                {"order": "Order could not be processed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            OrderResponseSerializer(order).data, status=status.HTTP_201_CREATED
        )
