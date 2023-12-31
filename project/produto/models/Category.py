from django.db import models
from django.utils.text import slugify
from .abstract import AbstractName

class Category(AbstractName):
    slug = models.SlugField(    
        "Link", max_length=120, unique=True, blank=True,
        help_text='Deixe vazio para gerar automaticamente.'
    )
    
    def save(self):
        self.slug = slugify(self.name) if not self.slug else slugify(self.slug)
        super(Category, self).save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'produto_categories'