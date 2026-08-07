from django.conf import settings
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

api_prefix = settings.API_ROOT_PREFIX.strip("/")

urlpatterns = [
    path("order/", include("order.urls")),
    path("order-item/", include("order_item.urls")),
    path(f"{api_prefix}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"{api_prefix}/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"{api_prefix}/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
