from typing import List
from produto.models.Unit import Unit
from django.shortcuts import get_object_or_404
from django.db.models import F 

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