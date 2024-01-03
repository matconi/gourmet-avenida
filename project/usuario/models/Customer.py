from django.db import models
from produto.models.abstract.AbstractName import AbstractName
from django.contrib.auth.models import Group
from . import User
from usuario.domain.repositories import role_repository
from django.utils import timezone
from datetime import date
from usuario.domain.services import messages_service
from typing import List

class Customer(AbstractName):
    class Gender(models.TextChoices):
        MALE = ('M', 'Masculino')
        FEMALE = ('F', 'Feminino')

    bill = models.DecimalField("Conta", max_digits=6, decimal_places=2, default=0)
    limit = models.DecimalField("Limite", max_digits=6, decimal_places=2, default=0,
        help_text='Define o valor máximo da conta à prazo. Válido apenas para Usuários Premium.'
    )
    gender = models.CharField("Gênero", max_length=2, choices=Gender.choices)
    born_at = models.DateField("Nascimento")

    user = models.OneToOneField("User", on_delete=models.CASCADE,
        verbose_name='Usuário', related_name='user_customer', blank=True, null=True
    )
    favorites = models.ManyToManyField("produto.Unit", blank=True, verbose_name='Favoritos', related_name='unit_favorite')

    def get_age(self) -> int:
        today = date.today()
        age = today.year - self.born_at.year - ((today.month, today.day) < (self.born_at.month, self.born_at.day))
    
    def has_user(self) -> bool:
        return self.user is not None

    def is_premium(self) -> bool:
        return self.has_user() and self.user.has_perm('usuario.buy_in_term')

    @staticmethod
    def get_customer_roles_ids() -> List[int]:
        return [User.CUSTOMER_ROLE, User.CUSTOMER_PREMIUM_ROLE]

    def delete(self):
        if self.has_user():
            customer_roles_ids = Customer.get_customer_roles_ids()
            roles = role_repository.get_by_ids(customer_roles_ids)
            for role in roles:
                role_repository.remove(self.user, role)
        super(Customer, self).delete()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'usuario_customers'
        permissions = [
            ("payments", "Can view self payments",),
            ("favorites", "Can view favorites",),
            ("add_favorite", "Can add favorite",),
            ("remove_favorite", "Can remove favorite",),
            ("buy_in_term", "Can buy in term",)
        ]