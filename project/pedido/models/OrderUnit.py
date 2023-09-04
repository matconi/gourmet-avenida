from django.db import models

class OrderUnit(models.Model):
    quantity = models.PositiveIntegerField("Quantidade", default=1)

    order = models.ForeignKey("Order", on_delete=models.CASCADE,
        verbose_name='Pedido', db_column='order_id'
    )
    unit = models.ForeignKey("produto.Unit", on_delete=models.RESTRICT,
        verbose_name='Unidade', db_column='unit_id'
    )
    
    def __str__(self) -> str:
        return f"Item {self.pk}"

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
        db_table = 'pedido_order_units'