from usuario.models.Customer import Customer
from usuario.models.User import User

def get_by_user(user: User) -> Customer:
    return Customer.objects.get(user=user)