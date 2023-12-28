from django.db import models
from .abstract import AbstractName
from django.utils.text import slugify

class Product(AbstractName):
    description = models.TextField("Descrição", max_length=400)
    slug = models.SlugField(
        "Link", max_length=120, unique=True, blank=True,
        help_text='Deixe vazio para gerar automaticamente.'
    )

    category = models.ForeignKey("Category", on_delete=models.RESTRICT, 
        verbose_name="Categoria"
    )

    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)

        super(Product, self).save()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        db_table = 'produto_products'