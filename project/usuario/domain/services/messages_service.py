from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from produto.models import Unit

def updated_profile(request) -> None:
    messages.success(
        request, 
        "Perfil alterado com sucesso."
    )

def password_reset_done(request) -> None:
    messages.success(
        request,
        "Email de redefinição de senha enviado com sucesso."
    )

def favorite_added(unit: Unit) -> str:
   return f'"{unit.name}" adicionado aos favoritos.'

def favorite_removed(unit: Unit) -> str:
   return f'"{unit.name}" removido dos favoritos.'