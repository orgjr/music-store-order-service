from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from order_item.serializers import OrderItemSerializer

from .config import TAG, VALIDATION_RESPONSE

create_schema = extend_schema(
    summary="Create an order item",
    description=(
        "Adds a new item to an existing order. The `product_code` field is "
        "generated automatically and must not be sent."
    ),
    tags=TAG,
    request=OrderItemSerializer,
    responses={
        201: OpenApiResponse(
            response=OrderItemSerializer,
            description="Order item created successfully.",
            examples=[
                OpenApiExample(
                    "Order item created",
                    summary="Newly created item",
                    value={
                        "id": 1,
                        "order": "3f9c2d1a-7b4e-4f6a-9c2d-1a7b4e4f6a9c",
                        "product_code": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
                        "product_name": "Vinyl — Kind of Blue, Miles Davis",
                        "product_description": "Remastered edition on 180g vinyl.",
                        "product_quantity": 2,
                        "item_price": "159.90",
                    },
                    response_only=True,
                ),
            ],
        ),
        400: VALIDATION_RESPONSE,
    },
    examples=[
        OpenApiExample(
            "New order item",
            summary="Body for creating an order item",
            value={
                "order": "3f9c2d1a-7b4e-4f6a-9c2d-1a7b4e4f6a9c",
                "product_name": "Vinyl — Kind of Blue, Miles Davis",
                "product_description": "Remastered edition on 180g vinyl.",
                "product_quantity": 2,
                "item_price": "159.90",
            },
            request_only=True,
        ),
    ],
)
