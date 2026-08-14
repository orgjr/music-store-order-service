from drf_spectacular.utils import OpenApiExample, OpenApiResponse

TAG = ["order"]

NOT_FOUND_RESPONSE = OpenApiResponse(
    description="Order not found for the informed uuid.",
    examples=[
        OpenApiExample(
            "Order not found",
            summary="Nonexistent uuid",
            value={"detail": "No order found for the informed uuid."},
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
            value={"customer_name": ["This field is required."]},
            response_only=True,
        ),
    ],
)
