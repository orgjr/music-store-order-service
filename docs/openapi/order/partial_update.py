from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from order.serializers import OrderSerializer

from .config import NOT_FOUND_RESPONSE, TAG, VALIDATION_RESPONSE

partial_update_schema = extend_schema(
    summary="Partially update an order",
    description="Updates one or more fields of an existing order.",
    tags=TAG,
    request=OrderSerializer(partial=True),
    responses={
        200: OpenApiResponse(
            response=OrderSerializer,
            description="Order updated successfully.",
            examples=[
                OpenApiExample(
                    "Order updated",
                    summary="Only the status was changed",
                    value={
                        "uuid": "3f9c2d1a-7b4e-4f6a-9c2d-1a7b4e4f6a9c",
                        "customer_id": "5e8b0c11-d2f3-4a5b-8c9d-1e2f3a4b5c6d",
                        "customer_name": "Marina Costa",
                        "price": "129.90",
                        "payment_type": "CC",
                        "status": "SHIPPED",
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
            "Partial update",
            summary="Minimal body to change the status",
            value={"status": "SHIPPED"},
            request_only=True,
        ),
    ],
)
