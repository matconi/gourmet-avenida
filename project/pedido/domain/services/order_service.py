from typing import List
from . import messages_service
from produto.models.Unit import Unit

def validate_avaliable(request, units: List[Unit], cart: dict) -> bool:
    is_valid = True
    for unit in units:
        unit_id = str(unit.id)
        avaliable = unit.avaliable()
        quantity_in_cart = cart[unit_id]["quantity"]

        if avaliable < quantity_in_cart:
            over_avaliable = quantity_in_cart - avaliable
            messages_service.over_avaliable(request, unit, over_avaliable)

            cart[unit_id]["quantity"] = avaliable
            cart[unit_id]["quantity_price"] = unit.quantity_price(avaliable)
         
            is_valid = False

    return is_valid 
