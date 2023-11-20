from usuario.models.Customer import Customer
from usuario.models.User import User

def get_by_user(user: User) -> Customer:
    return Customer.objects.get(user=user)

def create_by_user(user: User) -> None:
    Customer.objects.create(name=user.get_name(), user=user)
    