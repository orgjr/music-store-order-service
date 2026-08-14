from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from order_item.serializers import OrderItemSerializer

from .config import NOT_FOUND_RESPONSE, TAG

retrieve_schema = extend_schema(
    summary="Retrieve an order item",
    description="Returns the complete data of an order item by its id.",
    tags=TAG,
    responses={
        200: OpenApiResponse(
            response=OrderItemSerializer,
            description="Order item found.",
            examples=[
                OpenApiExample(
                    "Order item found",
                    summary="Example of a valid order item",
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
        404: NOT_FOUND_RESPONSE,
    },
)
