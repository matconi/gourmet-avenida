from django.template import Library

register = Library()

@register.filter
def total_in_cart(cart: dict) -> int:
    return sum(
        [
            unit["quantity"] for unit in cart.values()
        ]
    ) if cart else 0

@register.filter
def total_price_in_cart(cart: dict) -> float:
    return sum(
        [
            unit["quantity_price"] for unit in cart.values()
        ]
    )