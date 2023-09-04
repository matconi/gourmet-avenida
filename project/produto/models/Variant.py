from django.db import models
from .abstract.AbstractName import AbstractName

class Variant(AbstractName):

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Variante'
        verbose_name_plural = 'Variantes'
        db_table = 'produto_variants'