from django.utils import timezone
from typing import List
from pedido.models.Order import Order
from usuario.models.Customer import Customer
from usuario.domain.repositories import customer_repository
from produto.templatetags import pipe

def create_order(request, cart: dict) -> Order:
    return Order.objects.create(
        status=Order.Status.BOOKED,
        date_time=timezone.now(),
        total_price= pipe.total_price_in_cart(cart),
        total_quantity= pipe.total_in_cart(cart),
        customer=customer_repository.get_by_user(request.user)
    )

def get_user_orders(user) -> List[Order]:
    return Order.objects.filter(customer__user=user).prefetch_related('order_units__unit').order_by('-date_time')