from django.core.exceptions import ValidationError


def validate_product_price(product, item: dict) -> bool:
    if product["price"] != item["product_price"]:
        raise ValidationError(f"Product {item['product_name']} with inconsistent price")
    return True
