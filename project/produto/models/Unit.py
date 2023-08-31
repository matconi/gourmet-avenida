from django.db import models

class Unit(models.Model):
    name = models.CharField("Nome", max_length=100)
    sku = models.CharField("Código", max_length=12, unique=True)
    image = models.ImageField("Imagem", upload_to='produtos')

    price = models.DecimalField("Preço", max_digits=5, decimal_places=2)
    promotional = models.DecimalField("Preço promocional", max_digits=5, decimal_places=2, 
       blank=True, null=True
    )

    stock = models.PositiveIntegerField("Estoque")
    booked = models.PositiveIntegerField("Reservado", default=0)

    product = models.ForeignKey("Product", on_delete=models.RESTRICT, 
        verbose_name='Produto', db_column='product_id'
    )
    variations = models.ManyToManyField("Variation", blank=True, related_name='variations_units')

    def __avaliable(self) -> int:
        return self.stock - self.booked

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'
        db_table = 'produto_units'