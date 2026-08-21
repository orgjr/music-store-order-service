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
            summary="Missing checkout reference",
            value={"cart": ["This field is required."]},
            response_only=True,
        ),
    ],
)

PROCESSING_ERROR_RESPONSE = OpenApiResponse(
    description=(
        "The order could not be processed because a dependent service, product "
        "validation, or database operation failed."
    ),
    examples=[
        OpenApiExample(
            "Processing error",
            value={"order": "Order could not be processed"},
            response_only=True,
        ),
    ],
)
