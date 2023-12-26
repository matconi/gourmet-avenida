from typing import List
from produto.models.Unit import Unit
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils import timezone
from django.db.models import F
from usuario.models.Customer import Customer
from pedido.models import OrderUnit

def get_showcase(kwargs: dict) -> List[Unit]:
    return (
        Unit.objects.filter(showcase=True, **kwargs)
        .annotate(uid=F('id'), category_slug=F('product__category__slug'), product_slug=F('product__slug'))
        .select_related('product__category')
    )

def get_index(kwargs: dict={}) -> List[Unit]:
    return get_showcase(kwargs)

def get_index_category(category_slug: str, kwargs: dict={}) -> List[Unit]:
    conditions = {"product__category__slug": category_slug}
    conditions.update(kwargs)
    return get_showcase(conditions)

def get_related_category(category_slug: str, product_id) -> List[Unit]:
    return (
        Unit.objects.filter(product__category__slug=category_slug)
        .annotate(uid=F('id'), category_slug=F('product__category__slug'), product_slug=F('product__slug'))
        .exclude(product__id=product_id)
    )

def get_or_404(id: int) -> Unit:
    return get_object_or_404(Unit, id=id)

def get_by_id(id: int) -> Unit:
    return Unit.objects.get(id=id)

def get_all_by_id(id_list: List[int]) -> List[Unit]:
    return Unit.objects.filter(id__in=id_list).all()

def get_releases() -> List[Unit]: 
    last_month = (timezone.now() - timedelta(days=31)).date()
     
    return (
        Unit.objects.filter(showcase=True, released__gte=last_month)
        .annotate(uid=F('id'), category_slug=F('product__category__slug'), product_slug=F('product__slug'))
        .order_by('-released')[:10]
    )

def get_customer_favorites(customer: Customer, kwargs: dict={}) -> List[Unit]:
    return (
        Unit.objects.filter(unit_favorite=customer, **kwargs)
        .annotate(uid=F('id'), category_slug=F('product__category__slug'), product_slug=F('product__slug'))
        .all()
    )

def up_booked(unit: Unit, to_book: int) -> None:
    unit.booked += to_book
    unit.save()

def down_booked(order_unit: OrderUnit) -> None:
    unit = order_unit.unit
    prev = unit.booked - order_unit.quantity
    unit.booked = prev if prev >= 0 else 0
    unit.save()

CARDS_PER_VIEW = 12