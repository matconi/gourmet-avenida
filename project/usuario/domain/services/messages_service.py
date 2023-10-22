from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse

def uncomplete_register(request) -> None:
    messages.warning(
        request, format_html(
            "Complete o cadastro para acessar mais funcionalidades <a href={}> aqui.</a>", 
            reverse('produto:index')
        ) 
    )