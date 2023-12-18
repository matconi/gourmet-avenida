from django.db import models
from .abstract import AbstractName

class Variety(AbstractName):

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Variedade'
        verbose_name_plural = 'Variedades'
        db_table = 'produto_varieties'