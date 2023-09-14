from produto.models.Product import Product
from produto.models.Unit import Unit

def get_all():
    return Unit.objects.filter(showcase=True).all()