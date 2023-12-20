from django.db import models
from django.utils import timezone

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

    total_price = models.DecimalField("Preço Total", max_digits=5, decimal_places=2)
    total_quantity = models.PositiveIntegerField("Quantidade Total")
    discount = models.DecimalField("Desconto", max_digits=5, decimal_places=2, default=0)

    customer = models.ForeignKey("usuario.Customer", on_delete=models.RESTRICT,
        verbose_name='Cliente'
    )
    payment = models.ForeignKey("usuario.Payment", on_delete=models.RESTRICT,
        blank=True, null=True, default=None, verbose_name='Pagamento'
    )

    def get_bill(self) -> float:
        return self.total_price - self.discount

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