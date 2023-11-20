from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse

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