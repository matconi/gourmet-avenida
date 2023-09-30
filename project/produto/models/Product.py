from django.db import models
from .abstract.AbstractName import AbstractName
from django.utils.text import slugify

class Product(AbstractName):
    description = models.CharField("Descrição", max_length=400)
    slug = models.SlugField("Link", max_length=120)

    category = models.ForeignKey("Category", on_delete=models.RESTRICT, 
        verbose_name="Categoria"
    )

    def save(self):
        self.slug = slugify(self.name)
        super(Product, self).save()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        db_table = 'produto_products'