from typing import List
from produto.models.Unit import Unit
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils import timezone
from django.db.models import F
from usuario.models.Customer import Customer

def get_showcase() -> List[Unit]:
    return (
        Unit.objects.filter(showcase=True)
        .annotate(uid=F('id'), product_slug=F('product__slug'))
        .select_related('product')
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
        Unit.objects.filter(released__gte=last_month)
        .annotate(uid=F('id'), product_slug=F('product__slug'))
        .order_by('-released')[:10]
    )

def get_customer_favorites(customer: Customer) -> List[Unit]:
    return (
        Unit.objects.filter(unit_favorite=customer)
        .annotate(uid=F('id'), product_slug=F('product__slug'))
        .all()
    )