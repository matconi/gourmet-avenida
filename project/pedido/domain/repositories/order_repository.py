from typing import List
from pedido.models.Order import Order
from usuario.models.Customer import Customer
from usuario.domain.repositories import customer_repository
from produto.templatetags import produto_pipe
from django.utils import timezone
from datetime import timedelta
from usuario.models import User
from django.shortcuts import get_object_or_404

def create_booking(request) -> Order:
    cart = request.session["cart"]
    return Order.objects.create(
        status=Order.Status.BOOKED,
        booked_upto=timezone.now() + timedelta(days=2),
        total_price= produto_pipe.total_price_in_cart(cart),
        total_quantity= produto_pipe.total_in_cart(cart),
        customer=customer_repository.get_by_user(request.user)
    )

def get_user_orders(user: User, kwargs: dict) -> List[Order]:
    status_list = [Order.Status.FINISHED, Order.Status.BOOKED, Order.Status.EXPIRED, Order.Status.REPROVED]
    return (
        Order.objects.filter(customer__user=user, status__in=status_list, **kwargs)
        .prefetch_related('order_units__unit__product__category')
    )

def get_booked_by_user(user: User) -> List[Order]:
    return Order.objects.filter(customer__user=user, status=Order.Status.BOOKED)

def get_or_404(id: str) -> Order:
    return get_object_or_404(Order, id=id)

def change_status(order: Order, status: str) -> None:
    order.status = status
    order.save()