from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse

from produto.models.Unit import Unit

def over_avaliable(request, unit: Unit, over_avaliable: int) -> None:
    messages.warning(
        request,
        f'Atualmente seu carrinho possui mais unidades de "{unit.name}" que o disponível. '
        f'Reduzimos {over_avaliable}x do seu carrinho.'   
    ) 