from produto.models.Unit import Unit
from typing import List

def get_units_variations(slug: str) -> List[Unit]:
    return Unit.objects.filter(product__slug=slug).prefetch_related('variations')

def get_variations_values(units: List[Unit]) -> List[dict]:
    return units.values(
        'variations__id', 'variations__name', 
        'variations__variant__id', 'variations__variant__name'
    ).distinct() 