from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from docs.openapi.config import paginated_response
from order.serializers import OrderSerializer

from .config import TAG

list_schema = extend_schema(
    summary="List orders",
    description=(
        "Returns the paginated list of registered orders, from the most "
        "recent to the oldest."
    ),
    tags=TAG,
    responses={
        200: OpenApiResponse(
            response=paginated_response(OrderSerializer),
            description="Paginated list of orders.",
            examples=[
                OpenApiExample(
                    "Order list",
                    summary="Paginated response with one order",
                    value={
                        "count": 1,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "uuid": "3f9c2d1a-7b4e-4f6a-9c2d-1a7b4e4f6a9c",
                                "customer_id": "5e8b0c11-d2f3-4a5b-8c9d-1e2f3a4b5c6d",
                                "customer_name": "Marina Costa",
                                "price": "129.90",
                                "payment_type": "CC",
                                "status": "PENDING",
                                "items": [],
                                "created_at": "2026-08-07T14:30:00-03:00",
                            }
                        ],
                    },
                    response_only=True,
                ),
            ],
        )
    },
)
