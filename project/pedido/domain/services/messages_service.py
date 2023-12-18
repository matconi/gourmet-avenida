from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from produto.models import Unit
from pedido.models import Order

def empty_cart() -> str:
    return "Atualmente o seu carrinho se encontra vazio!"
    
def units_not_found() -> str:
    return f"Um ou mais itens presentes do carrinho não foram encontrados!"
    f" Talvez tenham sido apagados."

def over_avaliable( unit: Unit, over_avaliable: int) -> str:
    return f'Atualmente seu carrinho possui mais unidades de "{unit.name}" que o disponível. '
    f'Reduzimos {over_avaliable}x do seu carrinho.'   

def booked_success() -> str:
    return format_html(
        'Produtos reservados com sucesso.<a href="{}?status={}"> Visualizar.</a>', 
        reverse('pedido:index'), Order.Status.BOOKED
    )