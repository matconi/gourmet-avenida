from django.db import models
from django.utils.text import slugify
from .abstract.AbstractName import AbstractName

class Category(AbstractName):
    slug = models.SlugField(max_length=120, editable=False)
    
    def save(self):
        self.slug = slugify(self.name)
        super(Category, self).save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'produto_categories'