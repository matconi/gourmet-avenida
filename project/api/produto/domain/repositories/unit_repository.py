from produto.models.Unit import Unit
from typing import List
from produto.domain.repositories.unit_repository import get_index, get_index_category, get_customer_favorites, CARDS_PER_VIEW

def get_units_variations(slug: str) -> List[Unit]:
    return Unit.objects.filter(product__slug=slug).prefetch_related('variations', 'unit_favorite').select_related('product__category')

def get_variations_values(units: List[Unit]) -> List[dict]:
    return units.values(
        'variations__id', 'variations__name', 
        'variations__variety__id', 'variations__variety__name'
    ).distinct()