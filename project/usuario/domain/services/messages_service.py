from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from produto.models import Unit
from usuario.models import Payment, Customer
from django.conf import settings
from produto.templatetags.produto_pipe import currencyformat

def updated_profile(request) -> None:
    messages.success(
        request, 
        "Perfil alterado com sucesso."
    )

def password_reset_done(request) -> None:
    messages.info(
        request,
        "Email de redefinição de senha enviado. Confira no email se foi digitado corretamente."
    )

def favorite_added(unit: Unit) -> str:
   return f'"{unit.name}" adicionado aos favoritos.'

def favorite_removed(unit: Unit) -> str:
   return f'"{unit.name}" removido dos favoritos.'

def pay_bill(request, customer: Customer) -> str:
    messages.success(request,
        format_html('O Pagamento foi vinculado à conta do cliente "{}" com sucesso.<a href="{}">Alterar</a>', 
        customer.name, f'/{settings.ADMIN_PATH}usuario/customer/{customer.pk}/change/')
    )

def update_pay_bill(request, customer: Customer, diff: float) -> str:
    messages.warning(request,
        format_html('Atenção! A conta do cliente "{}" foi {} com a diferença' 
        ' do valor inicial para o editado: {}.<a href="{}">Alterar</a>', 
        customer.name, 'reduzida' if diff > 0 else 'acrescida', 
        currencyformat(abs(diff)), f'/{settings.ADMIN_PATH}usuario/customer/{customer.pk}/change/')
    )