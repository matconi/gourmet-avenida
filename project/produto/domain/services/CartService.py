from . import messages_service
from produto.models.Unit import Unit
from django.core.validators import ValidationError

class CartService:
    def __init__(self, request):
        self.request = request
        cart = self.request.session.get('cart')
        self.messages = {
            "success": [],
            "info": [],
            "warning": [],
            "danger": []
        }

        if not cart:
            cart = self.request.session["cart"] = {}
        self.cart = cart

    def get_messages(self) -> dict:
        return self.messages

    def add(self, unit: Unit, quantity: str) -> None:
        unit_id = str(unit.id)
        quantity = int(quantity)

        quantity_added = self.__add_new_unit(unit, quantity, unit_id) \
            if unit_id not in self.cart \
            else self.__add_existing_unit(unit, quantity, unit_id)

        if quantity_added > 0:
            self.__added_success(quantity_added, unit)
        
    def __added_success(self, quantity_in_cart: int, unit: Unit) -> None:
        self.save()
        self.messages["success"].append(messages_service.added_to_cart(unit, quantity_in_cart))

        if quantity_in_cart == unit.avaliable():
            self.messages["warning"].append(messages_service.all_avaliable_warn(unit))
  
    def __add_new_unit(self, unit: Unit, quantity: int, unit_id: str) -> int:
        quantity_in_cart = quantity
        avaliable = unit.avaliable()
        if avaliable == 0:
            self.messages["danger"].append(messages_service.empty_avaliable(unit))
            return 0

        elif quantity_in_cart > avaliable:
            self.messages["warning"].append(messages_service.not_enough_to_add(quantity, unit, avaliable))

            quantity_in_cart = avaliable
            
        quantity_price = unit.quantity_price(quantity_in_cart)
            
        self.cart[unit_id] = {
            "id": unit.id,
            "name": unit.name,
            "price": float(unit.price), 
            "quantity": quantity_in_cart,
            "quantity_price": quantity_price,
            "slug": unit.product.slug,
            "category": unit.product.category.slug
        }
        return quantity_in_cart

    def __add_existing_unit(self, unit: Unit, quantity: int, unit_id: str) -> int:
        quantity_in_cart = int(self.cart[unit_id]["quantity"])
        quantity_price = float(self.cart[unit_id]["quantity_price"])
        
        avaliable = unit.avaliable()
        try:
            self.__existing_cart_validation(quantity_in_cart, quantity, avaliable, unit, unit_id)
        except ValidationError:
            return 0

        quantity_in_cart += quantity
        if quantity_in_cart > avaliable:
            quantity_added = avaliable - self.cart[unit_id]["quantity"]

            self.messages["warning"].append(messages_service.not_enough_to_add(
                quantity_in_cart, unit, quantity_added  
            ))

            quantity_in_cart = avaliable
        
        quantity_price = unit.quantity_price(quantity_in_cart)
        
        self.cart[unit_id]["quantity"] = quantity_in_cart
        self.cart[unit_id]["quantity_price"] = quantity_price
        return quantity_in_cart

    def __existing_cart_validation(self, quantity_in_cart: int, quantity: int, avaliable: int, unit: Unit, unit_id: str):
        if avaliable == 0:
            self.messages["danger"].append(messages_service.not_enough_removed(unit))
            
            self.remove(unit)
            self.save()
            raise ValidationError("No avaliable product now")

        elif quantity_in_cart == avaliable and quantity > 0:
            self.messages["warning"].append(messages_service.all_avaliable_warn(unit))

            raise ValidationError("All avaliable product now")

        elif quantity_in_cart > avaliable:
            over_avaliable = quantity_in_cart - avaliable

            self.messages["warning"].append(messages_service.over_avaliable(unit, over_avaliable))
            self.messages["warning"].append(messages_service.all_avaliable_warn(unit))

            quantity_in_cart -= over_avaliable
            quantity_price = unit.quantity_price(quantity_in_cart)
              
            self.cart[unit_id]["quantity"] = quantity_in_cart
            self.cart[unit_id]["quantity_price"] = quantity_price

    def save(self) -> None:
        self.request.session.modified = True

    def remove(self, unit: Unit) -> None:
        del self.cart[str(unit.id)]
        self.save()
        self.messages["success"].append(messages_service.removed_unit(unit))

    def clean(self) -> None:
        del self.request.session["cart"]
        self.save()
        self.messages["success"].append(messages_service.cleaned_cart())