from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField("Nome", max_length=60)
    description = models.CharField("Descrição", max_length=400)
    slug = models.SlugField(max_length=90, verbose_name='Link')

    category = models.ForeignKey("Category", on_delete=models.RESTRICT, 
        verbose_name="Categoria", db_column='category_id'
    )

    # def save(self):
    #     self.slug = slugify(self.name)
    #     super(Product, self).save()

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        db_table = 'produto_products'