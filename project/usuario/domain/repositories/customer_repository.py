from usuario.models import User, Customer, Payment
from produto.models import Unit
from usuario.domain.services import customer_service

def get_by_user(user: User) -> Customer:
    return Customer.objects.get(user=user)

def create_by_user(user: User) -> None:
    Customer.objects.create(name=user.get_name(), user=user)

def add_favorite(customer: Customer, unit: Unit) -> None:
    customer.favorites.add(unit)

def remove_favorite(customer: Customer, unit: Unit) -> None:
    customer.favorites.remove(unit)

def pay_bill(payment: Payment, diff: float=0) -> Customer:
    customer: Customer = payment.customer
    customer.bill -= payment.amount if diff == 0 else diff
    customer_service.validate_limit(customer)
    customer.save()
    return customer

def buy_bill(customer: Customer, total_price: float) -> Customer:
    customer.bill += total_price
    customer_service.validate_limit(customer)
    customer.save()
    return customer