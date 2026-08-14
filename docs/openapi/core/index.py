from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

index_schema = extend_schema(
    summary="Identifies the application",
    description=(
        "Returns the name, version, description and environment of the "
        "application, along with the documentation and health check URLs."
    ),
    tags=["core"],
    responses={
        200: OpenApiResponse(
            description="Application identification information.",
            examples=[
                OpenApiExample(
                    "Application index",
                    summary="Response with service metadata",
                    value={
                        "name": "Music Store Order Service",
                        "version": "0.9.0",
                        "description": (
                            "Service for managing orders in a music store, "
                            "exposing a REST API for orders and order items."
                        ),
                        "environment": "dev",
                        "redoc_url": "/api/v1/redoc/",
                        "health_url": "/api/v1/health/",
                        "api_version": "V1",
                    },
                    response_only=True,
                ),
            ],
        )
    },
)
