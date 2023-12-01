from django.db import models
from produto.models.abstract.AbstractName import AbstractName
from django.contrib.auth.models import Group
from . import User
from usuario.domain.repositories import role_repository

class Customer(AbstractName):
    bill = models.DecimalField("Conta", max_digits=5, decimal_places=2, default=0)
    limit = models.DecimalField("Limite", max_digits=5, decimal_places=2, default=0,
        help_text='Define o valor máximo da conta à prazo. Deixe vazio caso indefinido.'
    )

    user = models.OneToOneField("User", on_delete=models.CASCADE,
        verbose_name='Usuário', related_name='user_customer', blank=True, null=True
    )

    favorites = models.ManyToManyField("produto.Unit", blank=True, verbose_name='Favoritos', related_name='unit_favorite')

    def delete(self):
        if self.user:
            raise Exception(self.user.groups.filter(id=User.CUSTOMER_ROLE))

        super(Customer, self).delete()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'usuario_customers'
        permissions = [
            ("payments", "Can view self payments"),
            ("favorites", "Can view self payments"),
            ("add_favorite", "Can add favorite"),
            ("buy_in_term", "Can buy in term")
        ]