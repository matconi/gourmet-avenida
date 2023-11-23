from produto.models import Category
from typing import List

def get_all() -> List[Category]:
    return Category.objects.all()

def get_by_slug(slug: str) -> Category:
    return Category.objects.get(slug=slug)