from django.db import models
from django.utils import timezone
import decimal

class Order(models.Model):
    class Status(models.TextChoices):
        FINISHED = ('F', 'Finalizado')
        BOOKED = ('B', 'Reservado')
        EXPIRED = ('E', 'Expirado')
        REPROVED = ('R', 'Reprovado')
        CONSUMED = ('C', 'Consumido')
        ABANDONED = ('A', 'Cancelado')

    status = models.CharField("Status", max_length=1, choices=Status.choices, default=Status.FINISHED)
    date_time = models.DateTimeField("Data/Hora", default=timezone.now)
    booked_upto = models.DateTimeField("Reservado até", blank=True, null=True, default=None,
        help_text='Preencha apenas se estiver reservado'
    )

    total_price = models.DecimalField("Preço Total", max_digits=5, decimal_places=2, blank=True, default=0)
    total_quantity = models.PositiveIntegerField("Quantidade Total", blank=True, default=0)
    discount = models.DecimalField("Desconto", max_digits=5, decimal_places=2, default=0)

    customer = models.ForeignKey("usuario.Customer", on_delete=models.RESTRICT,
        verbose_name='Cliente'
    )
    payment = models.ForeignKey("usuario.Payment", on_delete=models.RESTRICT,
        blank=True, null=True, default=None, verbose_name='Pagamento'
    )

    def get_sold_price(self) -> float:
        return decimal.Decimal(self.total_price) - decimal.Decimal(self.discount)

    def set_total_price(self, order_units) -> float:
        self.total_price = sum([order_unit.unit.quantity_price(order_unit.quantity) for order_unit in order_units])

    def set_total_quantity(self, order_units) -> int:
        self.total_quantity = sum([order_unit.quantity for order_unit in order_units])

    def __str__(self) -> str:
        return f"Pedido {self.pk}"

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        db_table = 'pedido_orders'
        ordering = ["-date_time"]
        permissions = [
            ("self_orders", "Can view self orders"),
            ("cancel_book", "Can cancel booking")
        ]