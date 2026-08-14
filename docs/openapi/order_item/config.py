from drf_spectacular.utils import OpenApiExample, OpenApiResponse

TAG = ["order_item"]

NOT_FOUND_RESPONSE = OpenApiResponse(
    description="Order item not found for the informed id.",
    examples=[
        OpenApiExample(
            "Order item not found",
            summary="Nonexistent id",
            value={"detail": "No order item found for the informed id."},
            response_only=True,
        ),
    ],
)

VALIDATION_RESPONSE = OpenApiResponse(
    description="Invalid or incomplete input data.",
    examples=[
        OpenApiExample(
            "Validation error",
            summary="Missing required field",
            value={"product_name": ["This field is required."]},
            response_only=True,
        ),
    ],
)
