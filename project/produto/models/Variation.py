from django.db import models

class Variation(models.Model):
    name = models.CharField("Nome", max_length=45)

    variant = models.ForeignKey("Variant", on_delete=models.RESTRICT,
        verbose_name='Variante', db_column='variant_id'
    )

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
        db_table = 'produto_variations'