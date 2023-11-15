from pedido.models.Order import Order
from pedido.models.OrderUnit import OrderUnit
from produto.models.Unit import Unit
from produto.domain.repositories import unit_repository
from typing import List
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, F
from usuario.models.Customer import Customer

def create_order_units(order: Order, cart: dict) -> None:
    OrderUnit.objects.bulk_create(
        [
            OrderUnit(
                quantity=unit["quantity"],
                order=order,
                unit=unit_repository.get_by_id(unit["id"])
            ) for unit in cart.values()
        ]
    )

def get_week_trends() -> List[OrderUnit]: 
    last_week = (timezone.now() - timedelta(days=7)).date()
     
    return (
        OrderUnit.objects.filter(order__date_time__gte=last_week)
        .values(
            uid=F('unit__id'), 
            name=F('unit__name'), 
            image=F('unit__image'), 
            price=F('unit__price'), 
            promotional=F('unit__promotional'), 
            product_slug=F('unit__product__slug')
        )
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:10]
    )

def get_again(customer: Customer) -> List[Unit]: 
    last_45 = (timezone.now() - timedelta(days=45)).date()
     
    return (
        OrderUnit.objects.filter(order__date_time__gte=last_45, order__customer=customer)
        .values(
            uid=F('unit__id'), 
            name=F('unit__name'), 
            image=F('unit__image'), 
            price=F('unit__price'), 
            promotional=F('unit__promotional'), 
            product_slug=F('unit__product__slug')
        )
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:10]
    )