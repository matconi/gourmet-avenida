from django.shortcuts import render, redirect
from django.utils import timezone

from produto.models.Unit import Unit
from .models.Order import Order
from pedido.models.OrderUnit import OrderUnit
from .domain.services import messages_service, order_service
from .domain.repositories import order_repository, order_unit_repository
from produto.domain.repositories import unit_repository
from django.contrib.auth.decorators import login_required, permission_required
from gourmetavenida.utils import paginate, is_ajax
from django.views.decorators.http import require_GET, require_POST

@require_POST
@login_required
@permission_required('pedido.add_order', raise_exception=True)
def save(request):
    cart = request.session.get('cart')
    
    units_ids = [unit_id for unit_id in cart]  
    units = unit_repository.get_all_by_id(units_ids)
    
    if not order_service.validate_avaliable(request, units, cart):
        request.session.save()
        return redirect('produto:cart')
    
    order = order_repository.create_order(request, cart)     
    order_unit_repository.create_order_units(order, cart)
    
    del request.session["cart"]

    return redirect('produto:cart')

@require_GET
@login_required
@permission_required('pedido.self_orders', raise_exception=True)
def index(request):
    kwargs = order_service.filter_orders(request)

    orders = order_repository.get_user_orders(request.user, kwargs)

    context = {
        "page_obj": paginate(request, orders),
    }

    return render(request, 'pedido/index.html', context)
