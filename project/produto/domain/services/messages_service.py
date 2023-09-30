from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from produto.models.Unit import Unit

def empty_avaliable(request, unit: Unit) -> None:
    messages.warning(
        request, format_html(                       
        'Nenhuma unidade de "{}" disponível no momento. <a href="{}"> Meu Carrinho.</a>',
        unit.name, reverse('produto:cart')
        )
    )   

def not_enough_to_add(request, quantity: int, unit: Unit, added: int) -> None:
    messages.warning(
        request,
        f'Disponibilidade insuficiente para {quantity}x do produto "{unit.name}". ' 
        f'Adicionamos {added}x no seu carrinho.'           
    )

def all_avaliable_warn(request, unit: Unit) -> None:
    messages.warning(
        request, format_html(                       
            'Atualmente seu carrinho possui todas as unidades de "{}" disponíveis. '
            'Recomendamos que finalize o pedido para garantir o produto.<a href="{}"> Meu Carrinho.</a>',
            unit.name, reverse('produto:cart')
        )
    )

def added_to_cart(request, unit: Unit, quantity: int) -> None:
    messages.success(
        request, format_html(
            'produto "{}" adicionado {}x no Carrinho.<a href="{}"> Confira.</a>',
            unit.name, quantity, reverse('produto:cart')
        )   
    )

def not_enough_removed(request, unit: Unit) -> None:
    messages.warning(
        request, format_html(                       
            'Nenhuma unidade de "{}" disponível no momento. O produto foi removido do carrinho<a href="{}"> Confira.</a>',
            unit.name, reverse('produto:cart')
        )
    )

def over_avaliable(request, unit: Unit, over_avaliable: int) -> None:
    messages.warning(
        self.request,
        f'Atualmente seu carrinho possui mais unidades de "{unit.name}" que o disponível. '
        f'Reduzimos {over_avaliable}x do seu carrinho.'   
    ) 