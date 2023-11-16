from django.db import models

class Customer(models.Model):
    bill = models.DecimalField("Conta", max_digits=5, decimal_places=2, 
        blank=True, null=True, default=None
    )
    limit = models.DecimalField("Limite", max_digits=5, decimal_places=2, 
        blank=True, null=True, default=None,
        help_text='Define o valor máximo da conta à prazo. Deixe vazio caso indefinido.'
    )

    user = models.OneToOneField("User", on_delete=models.RESTRICT, 
        verbose_name='Usuário', related_name='user_customer'
    )
    favorites = models.ManyToManyField("produto.Unit", blank=True, verbose_name='Favoritos', related_name='unit_favorite')

    def __str__(self) -> str:
        return self.user.get_name()

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'usuario_customers'