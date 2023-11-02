from django.shortcuts import render, redirect
from django.utils import timezone

from produto.models.Unit import Unit
from .models.Order import Order
from pedido.models.OrderUnit import OrderUnit
from .domain.services import messages_service, order_service
from .domain.repositories import order_repository, order_unit_repository
from produto.domain.repositories import unit_repository
from django.contrib.auth.decorators import login_required
from gourmetavenida.utils import paginate

@login_required
def save(request):
    if request.method == 'POST':
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

@login_required
def index(request):
    if request.method == 'GET':
        orders = order_repository.get_user_orders(request.user)
        page_obj = paginate(request, orders)

        context = {
           "page_obj": page_obj,
        }

        return render(request, 'pedido/index.html', context)
            
