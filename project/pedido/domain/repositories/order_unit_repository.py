from pedido.models import Order, OrderUnit
from produto.models import Unit
from produto.domain.repositories import unit_repository
from typing import List
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, F
from usuario.models.Customer import Customer
from produto.templatetags.produto_pipe import currencyformat

def create_booking_units(order: Order, cart: dict) -> None:
    OrderUnit.objects.bulk_create(
        [
            OrderUnit(
                quantity=unit["quantity"],
                price=unit["price"],
                order=order,
                unit=unit_repository.get_by_id(unit["id"])
            ) for unit in cart.values()
        ]
    )

def get_week_trends() -> List[OrderUnit]: 
    last_week = (timezone.now() - timedelta(days=7)).date()
     
    return (
        OrderUnit.objects.filter(order__date_time__gte=last_week, order__status=Order.Status.FINISHED)
        .values(
            uid=F('unit__id'), 
            name=F('unit__name'), 
            image_sm=F('unit__image_sm'),  
            uprice=F('unit__price'), 
            promotional=F('unit__promotional'),
            stock=F('unit__stock'),
            avaliable=F('unit__stock') - F('unit__booked'),
            category_slug=F('unit__product__category__slug'),
            product_slug=F('unit__product__slug')
        )
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:unit_repository.CARDS_PER_SLIDE]
    )

def get_again(customer: Customer) -> List[Unit]: 
    last_45 = (timezone.now() - timedelta(days=45)).date()
     
    return (
        OrderUnit.objects.filter(order__date_time__gte=last_45, order__customer=customer)
        .values(
            uid=F('unit__id'), 
            name=F('unit__name'), 
            image_sm=F('unit__image_sm'),
            uprice=F('unit__price'), 
            promotional=F('unit__promotional'),
            stock=F('unit__stock'),
            avaliable=F('unit__stock') - F('unit__booked'),
            category_slug=F('unit__product__category__slug'),
            product_slug=F('unit__product__slug')
        )
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:unit_repository.CARDS_PER_SLIDE]
    )

def get_by_order(order: Order) -> List[OrderUnit]:
    return OrderUnit.objects.filter(order=order).select_related('unit')