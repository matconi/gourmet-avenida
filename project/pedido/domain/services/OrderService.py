from typing import List, Dict
from . import messages_service
from produto.models import Unit
from gourmetavenida.utils import str_date_to_datetime
from django.core.validators import ValidationError
from produto.domain.repositories import unit_repository
from pedido.domain.repositories import order_repository, order_unit_repository

class OrderService():
    def __init__(self, request):
        self.request = request
        self.cart = self.request.session.get('cart')
        self.messages = {
            "success": [],
            "info": [],
            "warning": [],
            "danger": []
        }

    def get_messages(self) -> Dict[str, list]:
        return self.messages

    def book(self, units_ids: List[str]) -> None:
        self.__validate_empty_cart()
        units = unit_repository.get_all_by_id(units_ids)
        self.__validate_units_found(units, units_ids)
        self.__validate_avaliable(units)

        order = order_repository.create_booking(self.request)     
        order_unit_repository.create_booking_units(order, self.cart)
        del self.request.session["cart"]

        self.messages["success"].append(messages_service.booked_success())

    def __validate_empty_cart(self) -> None:
        if not self.cart:
            raise ValidationError(messages_service.empty_cart())

    def __validate_units_found(self, units, units_ids) -> None:
        if len(units) != len(units_ids):
            raise ValidationError(messages_service.units_not_found())

    def __validate_avaliable(self, units: List[Unit]) -> None:
        for unit in units:
            unit_id = str(unit.id)
            avaliable = unit.avaliable()
            quantity_in_cart = self.cart[unit_id]["quantity"]

            if avaliable < quantity_in_cart:
                self.cart[unit_id]["quantity"] = avaliable
                self.cart[unit_id]["quantity_price"] = unit.quantity_price(avaliable)
                self.request.session.modified = True

                over_avaliable = quantity_in_cart - avaliable
                raise ValidationError(messages_service.over_avaliable(unit, over_avaliable))
    
def filter_orders(request) -> dict:
    unit = request.GET.get('unit', '')
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
