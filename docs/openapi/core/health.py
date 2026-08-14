from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

health_schema = extend_schema(
    summary="Checks the service health",
    description=(
        "Returns the current process status, the local time in ISO 8601 and "
        "the server uptime in seconds."
    ),
    tags=["core"],
    responses={
        200: OpenApiResponse(
            description="Service is operational.",
            examples=[
                OpenApiExample(
                    "Health check ok",
                    summary="Response with a healthy status",
                    value={
                        "status": "ok",
                        "timestamp": "2026-08-07T14:30:00.123456-03:00",
                        "uptime_seconds": 42.12,
                    },
                    response_only=True,
                ),
            ],
        )
    },
)
