from usuario.models.Payment import Payment
from typing import List
from usuario.models.Customer import Customer

def get_customer_payments(customer: Customer, kwargs: dict) -> List[Payment]:
    return Payment.objects.filter(customer=customer, **kwargs).order_by('-date_time').all()