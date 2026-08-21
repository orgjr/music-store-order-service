from uuid import UUID

import requests
from django.conf import settings

from helpers.url import get_service_url


def request_user(customer: UUID) -> dict:
    base_url = get_service_url(name="customer", url=settings.CUSTOMER_SERVICE_URL)
    response = requests.get(f"{base_url}/{customer}/", timeout=5)
    response.raise_for_status()
    customer = response.json()
    return customer
