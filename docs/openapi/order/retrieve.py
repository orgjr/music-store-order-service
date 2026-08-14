from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from order.serializers import OrderSerializer

from .config import NOT_FOUND_RESPONSE, TAG

retrieve_schema = extend_schema(
    summary="Retrieve an order",
    description="Returns the complete data of an order by its uuid.",
    tags=TAG,
    responses={
        200: OpenApiResponse(
            response=OrderSerializer,
            description="Order found.",
            examples=[
                OpenApiExample(
                    "Order found",
                    summary="Example of a valid order",
                    value={
                        "uuid": "3f9c2d1a-7b4e-4f6a-9c2d-1a7b4e4f6a9c",
                        "customer_id": "5e8b0c11-d2f3-4a5b-8c9d-1e2f3a4b5c6d",
                        "customer_name": "Marina Costa",
                        "price": "129.90",
                        "payment_type": "CC",
                        "status": "PENDING",
                        "items": [
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
                        "created_at": "2026-08-07T14:30:00-03:00",
                    },
                    response_only=True,
                ),
            ],
        ),
        404: NOT_FOUND_RESPONSE,
    },
)
