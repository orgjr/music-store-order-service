from django.core.exceptions import ValidationError


def validate_stock(product: dict, item: dict) -> bool:
    if product["stock"] < item["quantity"]:
        raise ValidationError(
            f"There is no stock available for product: {item['product_name']}."
        )
    return True
