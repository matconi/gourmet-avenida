from . import messages_service
from produto.models.Unit import Unit
from django.core.validators import ValidationError
from typing import Dict

class CartService:
    def __init__(self, request):
        self.request = request
        cart = self.request.session.get('cart') 
        if not cart:
            cart = self.request.session["cart"] = {}
        self.cart = cart
        self.messages = {
            "success": [],
            "info": [],
            "warning": [],
            "danger": []
        } 

    def get_messages(self) -> Dict[str, list]:
        return self.messages

    def get_quantity_in_cart(self, unit_id: str) -> int:
        try:
            return int(self.cart[unit_id]["quantity"])
        except KeyError as e:
            return 0

    def add(self, unit: Unit, quantity_param: str) -> None:
        unit_id = str(unit.id)
        quantity_param = int(quantity_param)
        initial = self.get_quantity_in_cart(unit_id)
        if unit_id not in self.cart:
            self.__add_unit(unit, quantity_param, unit_id)
        else:
            self.__update_unit(unit, initial, quantity_param, unit_id)
        self.__saved_success(initial, unit, unit_id)
        
    def __saved_success(self, initial: int, unit: Unit, unit_id: str) -> None:
        self.save()
        current = self.get_quantity_in_cart(unit_id)
        if current != initial and current > 0:
            self.messages["success"].append(messages_service.added_to_cart(unit, current))

        if current == unit.avaliable():
            self.messages["warning"].append(messages_service.all_avaliable_warn(unit))

    def __is_avaliable(self, avaliable: int, compare: int=None) -> bool:
        return avaliable > 0 if compare is None else compare <= avaliable

    def __add_unit(self, unit: Unit, quantity_add: int, unit_id: str) -> None:
        avaliable = unit.avaliable()
        self.__validate_empty_avaliable(avaliable, unit)

        quantity_add = self.__add_quantity_in_cart(avaliable, unit, quantity_add)           
        self.__fill_add_unit_cart(unit_id, unit, quantity_add)  
    
    def __validate_empty_avaliable(self, avaliable: int, unit: Unit) -> None:
        if not self.__is_avaliable(avaliable):
            raise ValidationError(messages_service.empty_avaliable(unit))

    def __add_quantity_in_cart(self, avaliable: int, unit: Unit, quantity_add: int) -> int:
        if not self.__is_avaliable(avaliable, quantity_add):
            self.messages["warning"].append(messages_service.not_enough_to_add(quantity_add, unit, avaliable))
            quantity_add = avaliable

        return quantity_add

    def __fill_add_unit_cart(self, unit_id: str, unit: Unit, quantity_add: int) -> None:
        quantity_price = unit.quantity_price(quantity_add)
        self.cart[unit_id] = {
            "id": unit.id,
            "name": unit.name,
            "price": float(unit.price), 
            "quantity": quantity_add,
            "quantity_price": quantity_price,
            "slug": unit.product.slug,
            "category": unit.product.category.slug
        }

    def __update_unit(self, unit: Unit, quantity_in_cart: int, quantity_update: int, unit_id: str) -> None:
        avaliable = unit.avaliable()  
        self.__validate_empty_avaliable_remove(avaliable, unit, unit_id)

        quantity_in_cart += quantity_update     
        quantity_update = self.__update_quantity_in_cart(quantity_in_cart, avaliable, unit, unit_id)
        self.__fill_update_unit_cart(unit, quantity_update, unit_id)
        
    def __validate_empty_avaliable_remove(self, avaliable: int, unit: Unit, unit_id: str) -> None:
        if not self.__is_avaliable(avaliable):
            self.__remove_unit(unit_id)
            raise ValidationError(messages_service.not_enough_removed(unit))

    def __update_quantity_in_cart(self, quantity_update: int, avaliable: int, unit: Unit, unit_id: int) -> int:
        if not self.__is_avaliable(avaliable, quantity_update):
            quantity_added = avaliable - self.get_quantity_in_cart(unit_id)

            self.messages["warning"].append(messages_service.not_enough_to_add(
                quantity_update, unit, quantity_added  
            ))

            quantity_update = avaliable
        return quantity_update
    
    def __fill_update_unit_cart(self, unit: Unit, quantity_update: int, unit_id: str) -> None:
        quantity_price = unit.quantity_price(quantity_update)     
        self.cart[unit_id]["quantity"] = quantity_update
        self.cart[unit_id]["quantity_price"] = quantity_price

    def increment(self, unit: Unit) -> None:
        unit_id = str(unit.id)
        self.__validate_unit_in_cart(unit_id)
        
        initial = self.get_quantity_in_cart(unit_id)
        INCREMET = 1
        self.__update_unit(unit, initial, INCREMET, unit_id)
        self.__saved_success(initial, unit, unit_id)

    def __validate_unit_in_cart(self, unit_id: str) -> None:
        if not self.cart.get(unit_id):
            raise ValidationError(messages_service.not_found())

    def decrement(self, unit: Unit) -> None:
        unit_id = str(unit.id)
        self.__validate_unit_in_cart(unit_id)

        initial = self.get_quantity_in_cart(unit_id)
        if initial > 1 :
            self.__decrement_unit(unit, unit_id, initial)
            self.__saved_success(initial, unit, unit_id)
        else:
            self.remove(unit_id)
        
    def __decrement_unit(self, unit: Unit, unit_id: int, quantity_in_cart: int) -> None:
        avaliable = unit.avaliable()
        self.__validate_empty_avaliable_remove(avaliable, unit, unit_id)

        DECREMET = 1
        quantity_in_cart -= DECREMET
        quantity_decremented = self.__update_quantity_in_cart(quantity_in_cart, avaliable, unit, unit_id)
        self.__fill_update_unit_cart(unit, quantity_decremented, unit_id)

    def save(self) -> None:
        self.request.session.modified = True

    def remove(self, id: str) -> None:
        self.__validate_unit_in_cart(id)

        unit = self.cart.get(id)
        self.messages["success"].append(messages_service.removed_unit(unit))
        self.__remove_unit(id)
        self.save()

    def __remove_unit(self, id: str) -> None:
        del self.cart[id]

    def clean(self) -> None:
        del self.request.session["cart"]
        self.save()
        self.messages["success"].append(messages_service.cleaned_cart())