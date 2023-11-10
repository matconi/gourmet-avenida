from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse

def uncomplete_register(request) -> None:
    messages.warning(
        request, format_html(
            "Complete o cadastro para poder reservar produtos <a href={}> aqui.</a>", 
            reverse('usuario:profile')
        ) 
    )

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