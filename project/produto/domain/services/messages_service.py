from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from produto.models.Unit import Unit
from pedido.models import Order

def empty_avaliable(unit: Unit) -> str:
    return format_html(                       
        'Nenhuma unidade de "{}" disponível no momento. <a href="{}"> Visualizar.</a>',
        unit.name, reverse('produto:cart')
    )

def unique_active_book() -> str:
    return format_html(
        'Você já possui uma reserva ativa, não sendo possível adicionar produtos!<a href="{}?status={}"> Visualizar.</a>', 
        reverse('pedido:index'), Order.Status.BOOKED
    )
      
def not_enough_to_add(quantity: int, unit: Unit, added: int) -> str:
    return (f'Disponibilidade insuficiente para {quantity}x de "{unit.name}". ' 
            f'Adicionamos {added}x no seu carrinho.')           

def all_avaliable_warn(unit: Unit) -> str:
    return format_html(                       
        'Atualmente seu carrinho possui todas as unidades de "{}" disponíveis. <a href="{}"> Visualizar.</a>',
        unit.name, reverse('produto:cart')
    )

def added_to_cart(unit: Unit, quantity: int) -> str:
    return format_html(
        'Produto "{}" adicionado {}x no carrinho.<a href="{}"> Visualizar.</a>',
        unit.name, quantity, reverse('produto:cart')
    )   

def not_enough_removed(unit: Unit) -> str:
    return format_html(                       
        'Nenhuma unidade de "{}" disponível no momento. O produto foi removido do carrinho<a href="{}"> Visualizar.</a>',
        unit.name, reverse('produto:cart')
    )

def cleaned_cart() -> str:
    return 'Carrinho limpo com sucesso.'

def removed_unit(unit: Unit) -> str:
    return f'O produto "{unit["name"]}" foi removido com sucesso.'

def not_in_cart() -> str:
    return f'O produto não foi encontrado no carrinhho.'  