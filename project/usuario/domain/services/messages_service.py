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