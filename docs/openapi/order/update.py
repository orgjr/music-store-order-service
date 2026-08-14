from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from order.serializers import OrderSerializer

from .config import NOT_FOUND_RESPONSE, TAG, VALIDATION_RESPONSE

update_schema = extend_schema(
    summary="Update an order",
    description="Replaces every editable field of an existing order.",
    tags=TAG,
    request=OrderSerializer,
    responses={
        200: OpenApiResponse(
            response=OrderSerializer,
            description="Order updated successfully.",
            examples=[
                OpenApiExample(
                    "Order updated",
                    summary="Order with a changed status",
                    value={
                        "uuid": "3f9c2d1a-7b4e-4f6a-9c2d-1a7b4e4f6a9c",
                        "customer_id": "5e8b0c11-d2f3-4a5b-8c9d-1e2f3a4b5c6d",
                        "customer_name": "Marina Costa",
                        "price": "129.90",
                        "payment_type": "CC",
                        "status": "PAID",
                        "items": [],
                        "created_at": "2026-08-07T14:30:00-03:00",
                    },
                    response_only=True,
                ),
            ],
        ),
        400: VALIDATION_RESPONSE,
        404: NOT_FOUND_RESPONSE,
    },
    examples=[
        OpenApiExample(
            "Full update",
            summary="Body with every editable field",
            value={
                "customer_name": "Marina Costa",
                "price": "129.90",
                "payment_type": "CC",
                "status": "PAID",
            },
            request_only=True,
        ),
    ],
)
