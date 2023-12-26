from usuario.models import Customer
from django import forms
from produto.templatetags.produto_pipe import currencyformat

def validate_limit(customer: Customer) -> None:
    if customer.bill > customer.limit:
        raise forms.ValidationError(
            f'Atenção! A conta atual do cliente "{customer.name}", de {currencyformat(customer.bill)} ultrapassa o limite'
            f' de {currencyformat(customer.limit)}. Altere o limite para registrar o pagamento ou o rejeite.'
        )