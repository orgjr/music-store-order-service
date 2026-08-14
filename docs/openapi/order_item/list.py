from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from docs.openapi.config import paginated_response
from order_item.serializers import OrderItemSerializer

from .config import TAG

list_schema = extend_schema(
    summary="List order items",
    description=(
        "Returns the paginated list of registered order items, ordered by product name."
    ),
    tags=TAG,
    responses={
        200: OpenApiResponse(
            response=paginated_response(OrderItemSerializer),
            description="Paginated list of order items.",
            examples=[
                OpenApiExample(
                    "Order item list",
                    summary="Paginated response with one item",
                    value={
                        "count": 1,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "order": "3f9c2d1a-7b4e-4f6a-9c2d-1a7b4e4f6a9c",
                                "product_code": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
                                "product_name": "Vinyl — Kind of Blue, Miles Davis",
                                "product_description": "Remastered edition on 180g vinyl.",
                                "product_quantity": 2,
                                "item_price": "159.90",
                            }
                        ],
                    },
                    response_only=True,
                ),
            ],
        )
    },
)
