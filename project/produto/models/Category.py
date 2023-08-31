from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField("Nome", max_length=50)
    slug = models.SlugField("Link", max_length=80)
    
    supercategory = models.ForeignKey("self", on_delete=models.SET_NULL, 
        verbose_name='Subcategoria de ', db_column='supercategory_id',
        blank=True, null=True
    )

    # def save(self):
    #     self.slug = slugify(self.name)
    #     super(Product, self).save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'produto_categories'