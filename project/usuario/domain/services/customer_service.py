from usuario.models import Customer
from django import forms
from produto.templatetags.produto_pipe import currencyformat
from django.core.validators import ValidationError
from usuario.domain.repositories import customer_repository

def validate_limit(cleaned_data: dict) -> None:
    if cleaned_data["bill"] > cleaned_data["limit"]:
        raise ValidationError(
            f'Atenção! A conta atual do cliente {cleaned_data["name"]}, de {currencyformat(cleaned_data["bill"])}, ultrapassa o limite'
            f' de {currencyformat(cleaned_data["limit"])}. Altere o limite para prosseguir a operação ou rejeite.'
        )