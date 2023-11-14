from django.utils import timezone
from typing import List
from pedido.models.Order import Order
from usuario.models.Customer import Customer
from usuario.domain.repositories import customer_repository
from produto.templatetags import produto_pipe

def create_order(request, cart: dict) -> Order:
    return Order.objects.create(
        status=Order.Status.BOOKED,
        date_time=timezone.now(),
        total_price= produto_pipe.total_price_in_cart(cart),
        total_quantity= produto_pipe.total_in_cart(cart),
        customer=customer_repository.get_by_user(request.user)
    )

def get_user_orders(user, kwargs: dict) -> List[Order]:
    return Order.objects.filter(customer__user=user, **kwargs).prefetch_related('order_units__unit__product').order_by('-date_time')