from produto.models.Product import Product
from django.shortcuts import get_object_or_404

def get_by_slug(slug: str) -> Product:
    return get_object_or_404(Product, slug=slug)