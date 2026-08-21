from django.conf import settings

from helpers.get_request import get_request
from helpers.url import get_service_url

from .price import validate_product_price
from .stock import validate_stock


def validate_item(item: dict) -> None:
    base_url = get_service_url(name="catalog", url=settings.CATALOG_SERVICE_URL)
    product = get_request(url=base_url, params=item["product_slug"])
    validate_stock(product=product, item=item)
    validate_product_price(product=product, item=item)
