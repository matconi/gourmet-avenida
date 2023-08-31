from django.db import models

class Order(models.Model):
    class Status(models.TextChoices):
        FINISHED = ('F', 'Finalizado')
        BOOKED = ('B', 'Reservado')
        EXPIRED = ('E', 'Expirado')
        CONSUMED = ('C', 'Consumido')

    status = models.CharField("Status", max_length=1, choices=Status.choices, default=Status.FINISHED)

    total_price = models.DecimalField("Preço Total", max_digits=5, decimal_places=2)
    total_quantity = models.PositiveIntegerField("Quantidade Total")

    def __str__(self) -> str:
        return f"Pedido Nº {self.pk}."

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        db_table = 'pedido_orders'
