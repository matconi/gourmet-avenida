from pedido.models.Order import Order
from pedido.models.OrderUnit import OrderUnit
from produto.models.Unit import Unit
from produto.domain.repositories import unit_repository

def create_order_units(order: Order, cart: dict) -> None:
    OrderUnit.objects.bulk_create(
        [
            OrderUnit(
                quantity=unit["quantity"],
                order=order,
                unit=unit_repository.get_by_id(unit["id"])
            ) for unit in cart.values()
        ]
    )