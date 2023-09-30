from django.db import models
from .abstract.AbstractName import AbstractName

class Unit(AbstractName):
    sku = models.CharField("Código", max_length=12, unique=True)
    image = models.ImageField("Imagem", upload_to='produtos')

    price = models.DecimalField("Preço", max_digits=5, decimal_places=2)
    promotional = models.DecimalField("Preço promocional", max_digits=5, decimal_places=2, 
       blank=True, null=True, help_text='Preço acima do original que mostrará riscado.'
    )

    stock = models.PositiveIntegerField("Estoque")
    booked = models.PositiveIntegerField("Reservado", default=0)

    product = models.ForeignKey("Product", on_delete=models.RESTRICT, 
        verbose_name='Produto'
    )
    variations = models.ManyToManyField("Variation", blank=True, related_name='variations_units', verbose_name='Variações')
    showcase = models.BooleanField("Mostrar na vitrine", default=True)

    def avaliable(self) -> int:
        return self.stock - self.booked

    def quantity_price(self, quantity: int) -> float:
        return float(self.price * quantity)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
        db_table = 'produto_units'