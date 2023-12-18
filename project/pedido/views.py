from django.shortcuts import render, redirect
from django.utils import timezone
from .domain.services import OrderService
from .domain.services.OrderService import filter_orders
from .domain.repositories import order_repository, order_unit_repository
from produto.domain.repositories import unit_repository
from django.contrib.auth.decorators import login_required, permission_required
from gourmetavenida.utils import paginate, is_ajax
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse
from gourmetavenida.utils import try_method
from produto.templatetags import produto_pipe

@require_POST
@login_required
@permission_required('pedido.add_order', raise_exception=True)
def book(request):
    cart = request.session.get('cart')  
    units_ids = [unit_id for unit_id in cart]  

    order_service = OrderService(request)
    try_method(order_service, order_service.book, [units_ids])
    messages = order_service.get_messages()
    refresh_cart = request.session.get('cart')

    return JsonResponse({
        "messages": messages,
        "refresh_cart": {
            "cart": refresh_cart,
            "total_in_cart": produto_pipe.total_in_cart(refresh_cart),
            "total_price_in_cart": produto_pipe.total_price_in_cart(refresh_cart)
        }
    })

@require_GET
@login_required
@permission_required('pedido.self_orders', raise_exception=True)
def index(request):
    kwargs = filter_orders(request)

    orders = order_repository.get_user_orders(request.user, kwargs)

    context = {
        "page_obj": paginate(request, orders),
    }

    return render(request, 'pedido/index.html', context)
