from drf_spectacular.utils import extend_schema_view
from rest_framework.viewsets import ModelViewSet

from docs.openapi.order.create import create_schema
from docs.openapi.order.destroy import destroy_schema
from docs.openapi.order.list import list_schema
from docs.openapi.order.partial_update import partial_update_schema
from docs.openapi.order.retrieve import retrieve_schema
from docs.openapi.order.update import update_schema

from .models import Order
from .serializers import OrderSerializer


@extend_schema_view(
    list=list_schema,
    create=create_schema,
    retrieve=retrieve_schema,
    update=update_schema,
    partial_update=partial_update_schema,
    destroy=destroy_schema,
)
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
