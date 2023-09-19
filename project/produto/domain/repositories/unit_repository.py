from typing import List
from produto.models.Unit import Unit

def get_showcase() -> List[Unit]:
    return Unit.objects.filter(showcase=True).select_related('product')