from django.db import models
from django.utils.text import slugify
from .abstract import AbstractName

class Category(AbstractName):
    slug = models.SlugField(    
        "Link", max_length=120, unique=True, blank=True,
        help_text='Deixe vazio para gerar automaticamente.'
    )
    
    def save(self):
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)

        super(Category, self).save()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'produto_categories'