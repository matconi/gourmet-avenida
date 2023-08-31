from django.db import models

class Variant(models.Model):
    name = models.CharField("Nome", max_length=45)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Variante'
        verbose_name_plural = 'Variantes'
        db_table = 'produto_variants'