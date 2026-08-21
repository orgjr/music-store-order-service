from drf_spectacular.utils import extend_schema

partial_update_schema = extend_schema(
    exclude=True,
)
