from . import messages_service
from produto.models.Unit import Unit
from django.core.validators import ValidationError

class CartService:
    def __init__(self, request):
        self.request = request
        cart = self.request.session.get('cart')

        if not cart:
            cart = self.request.session["cart"] = {}
        self.cart = cart

    def add(self, unit: Unit, quantity: str) -> None:
        unit_id = str(unit.id)
        quantity = int(quantity)
        quantity_in_cart = self.__add_new_unit(unit, quantity, unit_id) \
            if unit_id not in self.cart \
            else self.__add_existing_unit(unit, quantity, unit_id)

        if quantity_in_cart > 0:
            self.__added_success(quantity_in_cart, unit)

    def __added_success(self, quantity_in_cart: int, unit: Unit) -> None:
        self.save()
        messages_service.added_to_cart(self.request, unit, quantity_in_cart)

        if quantity_in_cart == unit.avaliable():
            messages_service.all_avaliable_warn(self.request, unit)  

    def __add_new_unit(self, unit: Unit, quantity: int, unit_id: str) -> int:
        quantity_in_cart = quantity
        avaliable = unit.avaliable()
        if avaliable == 0:
            messages_service.empty_avaliable(self.request, unit)
            return 0

        elif quantity_in_cart > avaliable:
            messages_service.not_enough_to_add(self.request, quantity, unit, avaliable)
            quantity_in_cart = avaliable
            
        quantity_price = unit.quantity_price(quantity_in_cart)
            
        self.cart[unit_id] = {
            "id": unit.id,
            "name": unit.name,
            "price": float(unit.price), 
            "quantity": quantity_in_cart,
            "quantity_price": quantity_price,
            "image": unit.image.url,
            "slug": unit.product.slug
        }
        return quantity_in_cart

    def __add_existing_unit(self, unit: Unit, quantity: int, unit_id: str) -> int:
        quantity_in_cart = int(self.cart[unit_id]["quantity"])
        quantity_price = float(self.cart[unit_id]["quantity_price"])
        
        avaliable = unit.avaliable()
        try:
            self.__existing_cart_validation(quantity_in_cart, avaliable, unit, unit_id)
        except ValidationError:
            return 0

        quantity_in_cart += quantity           
        if quantity_in_cart > avaliable:
            messages_service.not_enough_to_add(
                self.request, quantity_in_cart, unit, 
                avaliable - self.cart[unit_id]["quantity"]
            )       
            quantity_in_cart = avaliable
        
        quantity_price = unit.quantity_price(quantity_in_cart)
        
        self.cart[unit_id]["quantity"] = quantity_in_cart
        self.cart[unit_id]["quantity_price"] = quantity_price
        return quantity_in_cart

    def __existing_cart_validation(self, quantity_in_cart: int, avaliable: int, unit: Unit, unit_id: str):
        if avaliable == 0:
            messages_service.not_enough_removed(self.request, unit)
            self.remove(unit_id)
            self.save()
            raise ValidationError("No avaliable product now")

        elif quantity_in_cart == avaliable: 
            messages_service.all_avaliable_warn(self.request, unit)
            raise ValidationError("All avaliable products now")

        elif quantity_in_cart > avaliable:
            over_avaliable = quantity_in_cart - avaliable
            messages_service.over_avaliable(self.request, unit, over_avaliable) 
            messages_service.all_avaliable_warn(self.request, unit) 

            quantity_in_cart -= over_avaliable
            quantity_price = unit.quantity_price(quantity_in_cart)
              
            self.cart[unit_id]["quantity"] = quantity_in_cart
            self.cart[unit_id]["quantity_price"] = quantity_price
            raise ValidationError("More products than avaliable now")

    def save(self):
        self.request.session.modified = True

    def remove(self, unit_id: int, unit: Unit) -> None:
        del self.cart[str(unit_id)]
        self.save()
        messages_service.removed_unit(self.request, unit)

    def clear(self) -> None:
        del self.request.session["cart"]
        self.save()
        messages_service.cleaned_cart(self.request)