from rest_framework.exceptions import ValidationError


def get_service_url(name, url):
    base_url = url.rstrip("/")
    if not base_url:
        raise ValidationError(f"{name} service is not configured.")

    return base_url
