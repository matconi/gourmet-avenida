from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from produto.models import Unit
from pedido.models import Order
from usuario.models import Payment, Customer
from django.conf import settings
from produto.templatetags.produto_pipe import currencyformat

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

def is_not_booked() -> str:
    return "Apenas é possível cancelar um pedido que está reservado!"

def canceled_success(request) -> None:
    messages.success(
        request,
        "O pedido foi cancelado com sucesso."
    )

def binded_order_payment(request, payment: Payment) -> None:
    messages.success(request,
        format_html('Pagamento PIX de {} vinculado ao pedido com sucesso. <a href="{}">Alterar</a>', 
        currencyformat(payment.amount), f'/{settings.ADMIN_PATH}usuario/payment/{payment.pk}/change/')
    )

def changed_bill(request, customer: Customer) -> None:
    messages.success(request,
        format_html('A conta do cliente "{}" foi acrescida com sucesso.<a href="{}">Alterar</a>', 
        customer.name, f'/{settings.ADMIN_PATH}usuario/customer/{customer.pk}/change/')
    )

def increased_booking(request) -> None:
    messages.info(request, "As unidades do pedido foram reservadas.")

def removed_booking(request) -> None:
    messages.info(request, "As unidades reservadas voltaram a ficar disponíveis.")