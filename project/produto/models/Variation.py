from django.db import models
from .abstract.AbstractName import AbstractName

class Variation(AbstractName):
    variety = models.ForeignKey("Variety", on_delete=models.RESTRICT,
        verbose_name='Variedade'
    )

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
        db_table = 'produto_variations'