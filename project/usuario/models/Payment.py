from django.db import models
from django.utils import timezone

class Payment(models.Model):
    class Method(models.TextChoices):
        MONEY = ('M', 'Dinheiro')
        PIX = ('P', 'Pix')
        CARD = ('C', 'Cartão')

    amount = models.DecimalField("Quantia", max_digits=5, decimal_places=2)
    method = models.CharField("Método", max_length=1, choices=Method.choices, default=Method.PIX)
    date_time = models.DateTimeField("Data/Hora", default=timezone.now)

    customer = models.ForeignKey("Customer", on_delete=models.RESTRICT, 
        verbose_name='Ciente'
    )

    def __str__(self) -> str:
        return f"Pagamento Nº {self.id}"

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        db_table = 'usuario_payments'