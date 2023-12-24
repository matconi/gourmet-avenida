from usuario.models.Payment import Payment
from typing import List
from usuario.models.Customer import Customer
from pedido.models import Order

def get_customer_payments(customer: Customer, kwargs: dict) -> List[Payment]:
    return Payment.objects.filter(customer=customer, **kwargs).order_by('-date_time').all()

def bind_order_payment(instance: Order) -> Payment:
    return Payment.objects.create(
        amount=instance.get_sold_price(),
        customer=instance.customer
    )
