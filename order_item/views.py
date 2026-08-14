from drf_spectacular.utils import extend_schema_view
from rest_framework.viewsets import ModelViewSet

from docs.openapi.order_item.create import create_schema
from docs.openapi.order_item.destroy import destroy_schema
from docs.openapi.order_item.list import list_schema
from docs.openapi.order_item.partial_update import partial_update_schema
from docs.openapi.order_item.retrieve import retrieve_schema
from docs.openapi.order_item.update import update_schema

from .models import OrderItem
from .serializers import OrderItemSerializer


@extend_schema_view(
    list=list_schema,
    create=create_schema,
    retrieve=retrieve_schema,
    update=update_schema,
    partial_update=partial_update_schema,
    destroy=destroy_schema,
)
class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
