from django.template import Library
from pedido.models import Order

register = Library()

@register.filter
def currencyformat(currency: float) -> str:
    return f'R$ {currency:.2f}'.replace('.', ',')

@register.filter
def total_in_cart(cart: dict) -> int:
    return sum([unit["quantity"] for unit in cart.values()]) if cart else 0

@register.filter
def total_price_in_cart(cart: dict) -> float:
    return sum([unit["quantity_price"] for unit in cart.values()]) if cart else 0
    
@register.filter
def actual_order_price(order: Order) -> float:
    return order.get_sold_price()