from uuid import UUID

import requests
from django.conf import settings

from helpers.url import get_service_url


def request_cart(cart: UUID) -> dict:
    base_url = get_service_url(name="cart", url=settings.CART_SERVICE_URL)
    response = requests.get(f"{base_url}/{cart}/", timeout=5)
    response.raise_for_status()
    cart = response.json()
    return cart
