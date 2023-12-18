from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from produto.models import Unit

def empty_cart() -> None:
    return "Atualmente o seu carrinho se encontra vazio!"
    

def units_not_found() -> None:
    return (
        "Um ou mais itens presentes do carrinho não foram encontrados!"
        " Talvez tenham sido apagados."
    )

def over_avaliable( unit: Unit, over_avaliable: int) -> None:
    return (
        f'Atualmente seu carrinho possui mais unidades de "{unit.name}" que o disponível. '
        f'Reduzimos {over_avaliable}x do seu carrinho.'   
    )

def booked_success() -> str:
    return format_html('Produtos reservados com sucesso.<a href="{}"> Visualizar.</a>', reverse('pedido:index'))