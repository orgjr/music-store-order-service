from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


def paginated_response(serializer_class):
    return inline_serializer(
        name=f"Paginated{serializer_class.__name__}",
        fields={
            "count": serializers.IntegerField(help_text="Total number of records."),
            "next": serializers.URLField(
                allow_null=True, help_text="URL of the next page, or null."
            ),
            "previous": serializers.URLField(
                allow_null=True, help_text="URL of the previous page, or null."
            ),
            "results": serializer_class(many=True),
        },
    )
