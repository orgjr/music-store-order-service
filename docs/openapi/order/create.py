from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from order.serializers import OrderSerializer

from .config import TAG, VALIDATION_RESPONSE

create_schema = extend_schema(
    summary="Create an order",
    description=(
        "Creates a new order. The `uuid`, `customer_id` and `created_at` "
        "fields are generated automatically and must not be sent."
    ),
    tags=TAG,
    request=OrderSerializer,
    responses={
        201: OpenApiResponse(
            response=OrderSerializer,
            description="Order created successfully.",
            examples=[
                OpenApiExample(
                    "Order created",
                    summary="Newly created order",
                    value={
                        "uuid": "3f9c2d1a-7b4e-4f6a-9c2d-1a7b4e4f6a9c",
                        "customer_id": "5e8b0c11-d2f3-4a5b-8c9d-1e2f3a4b5c6d",
                        "customer_name": "Marina Costa",
                        "price": "129.90",
                        "payment_type": "CC",
                        "status": "PENDING",
                        "items": [],
                        "created_at": "2026-08-07T14:30:00-03:00",
                    },
                    response_only=True,
                ),
            ],
        ),
        400: VALIDATION_RESPONSE,
    },
    examples=[
        OpenApiExample(
            "New order",
            summary="Body for creating an order",
            value={
                "customer_name": "Marina Costa",
                "price": "129.90",
                "payment_type": "CC",
            },
            request_only=True,
        ),
    ],
)
