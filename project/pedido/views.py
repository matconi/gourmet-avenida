from django.shortcuts import redirect
from django.utils import timezone

from produto.models.Unit import Unit
from pedido.models.OrderUnit import OrderUnit
from .domain.services import messages_service, order_service
from .domain.repositories import order_repository, order_unit_repository
from produto.domain.repositories import unit_repository

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
        
        del self.request.session["cart"]

        return redirect('produto:cart')
            
