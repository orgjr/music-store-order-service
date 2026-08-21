import logging
from uuid import UUID

from django.conf import settings
from django.db.transaction import atomic
from django.utils import timezone

from helpers.request_cart import request_cart
from helpers.request_user import request_user
from helpers.url import get_service_url
from order.models import Order
from order_item.models import OrderItem
from validators.item import validate_item

logger = logging.getLogger(__name__)


class OrderService:
    @staticmethod
    def process(customer: UUID, cart: UUID, payment_type: str) -> Order:
        with atomic():
            customer = request_user(customer)
            order = Order(
                customer_id=customer["uuid"],
                customer_name=f"{customer['first_name']} {customer['last_name']}",
                customer_doc=customer["doc"],
            )
            order.save()
            cart = request_cart(cart)
            product_url = get_service_url(
                name="catalog", url=settings.CATALOG_SERVICE_URL
            )
            for item in cart["items"]:
                validate_item(item)
                order_item = OrderItem.objects.create(
                    order=order,
                    product_code=item["product_id"],
                    product_name=item["product_name"],
                    product_url=f"{product_url}/{item['product_slug']}",
                    product_price=item["product_price"],
                    product_quantity=item["quantity"],
                    price=item["price"],
                )
                order_item.save()
            order.price = cart["price"]
            order.payment_type = payment_type
            order.save(update_fields=["price", "payment_type"])

        logger.warning(
            f"Timestamp: {timezone.localtime()},\nOrder {order.uuid} created."
        )

        return order
