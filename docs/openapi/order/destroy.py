from drf_spectacular.utils import OpenApiResponse, extend_schema

from .config import NOT_FOUND_RESPONSE, TAG

destroy_schema = extend_schema(
    summary="Delete an order",
    description="Permanently deletes an order and all of its items.",
    tags=TAG,
    responses={
        204: OpenApiResponse(description="Order deleted successfully."),
        404: NOT_FOUND_RESPONSE,
    },
)
