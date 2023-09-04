from django.db import models
from django.utils import timezone

class Order(models.Model):
    class Status(models.TextChoices):
        FINISHED = ('F', 'Finalizado')
        BOOKED = ('B', 'Reservado')
        EXPIRED = ('E', 'Expirado')
        CONSUMED = ('C', 'Consumido')

    status = models.CharField("Status", max_length=1, choices=Status.choices, default=Status.FINISHED)
    date_time = models.DateTimeField("Data/Hora", default=timezone.now)

    total_price = models.DecimalField("Preço Total", max_digits=5, decimal_places=2)
    total_quantity = models.PositiveIntegerField("Quantidade Total")

    customer = models.ForeignKey("usuario.Customer", on_delete=models.RESTRICT,
        verbose_name='Cliente', db_column='customer_id'
    )

    def __str__(self) -> str:
        return f"Pedido Nº {self.pk}"

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        db_table = 'pedido_orders'
