from drf_spectacular.utils import OpenApiResponse, extend_schema

from .config import NOT_FOUND_RESPONSE, TAG

destroy_schema = extend_schema(
    summary="Delete an order item",
    description="Permanently deletes an order item from the order it belongs to.",
    tags=TAG,
    responses={
        204: OpenApiResponse(description="Order item deleted successfully."),
        404: NOT_FOUND_RESPONSE,
    },
)
