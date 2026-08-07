from django.conf import settings
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import uptime


def _build_url(name, fallback_path):
    try:
        return reverse(name)
    except NoReverseMatch:
        return f"/{settings.API_ROOT_PREFIX.strip('/')}/{fallback_path}"


@api_view(["GET"])
def index(request):
    api_version = settings.API_ROOT_PREFIX.strip("/").split("/")[-1].upper()
    return Response(
        {
            "name": settings.PROJECT_NAME,
            "version": settings.PROJECT_VERSION,
            "description": settings.PROJECT_DESCRIPTION,
            "environment": settings.ENVIRONMENT,
            "redoc_url": _build_url("redoc", "redoc/"),
            "health_url": _build_url("health", "health/"),
            "api_version": api_version,
        }
    )


@api_view(["GET"])
def health(request):
    uptime_seconds = (timezone.localtime() - uptime.START_TIME).total_seconds()
    return Response(
        {
            "status": "ok",
            "timestamp": timezone.localtime().isoformat(),
            "uptime_seconds": round(uptime_seconds, 2),
        }
    )
