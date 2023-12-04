from usuario.models.Customer import Customer
from usuario.models.User import User
from produto.models import Unit

def get_by_user(user: User) -> Customer:
    return Customer.objects.get(user=user)

def create_by_user(user: User) -> None:
    Customer.objects.create(name=user.get_name(), user=user)

def add_favorite(customer: Customer, unit: Unit) -> None:
    customer.favorites.add(unit)

def remove_favorite(customer: Customer, unit: Unit) -> None:
    customer.favorites.remove(unit)