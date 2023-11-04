from typing import List
from . import messages_service
from produto.models.Unit import Unit
from gourmetavenida.utils import str_date_to_datetime

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

def filter_orders(request) -> dict:
    unit = request.GET.get('unit') or ''
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    kwargs = {}
    _filter_unit(unit, kwargs)
    _filter_status(status, kwargs)
    _filter_date_time(start_date, end_date, kwargs)
    
    return kwargs

def _filter_unit(unit: str, kwargs: dict) -> None:
    if unit.strip():
        kwargs["order_units__unit__name__icontains"] = unit
        
def _filter_status(status: str, kwargs: dict) -> None:
    if status:
        kwargs["status"] = status

def _filter_date_time(start_date: str, end_date: str, kwargs: dict) -> None:
    if start_date and end_date:
        kwargs["date_time__range"] = (
            str_date_to_datetime(start_date), str_date_to_datetime(end_date),
        )
    elif start_date:
        kwargs["date_time__gte"] = str_date_to_datetime(start_date)
    elif end_date:
        kwargs["date_time__lte"] = str_date_to_datetime(end_date)
