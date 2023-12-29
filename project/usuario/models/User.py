from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from .manager.UserManager import CustomUserManager
from django.utils import timezone

class User(AbstractUser):
    username = username_validator = None

    first_name = models.CharField("Primeiro Nome", max_length=50, blank=False, null=False)
    last_name = models.CharField("Último Nome", max_length=120, blank=True, null=True, default=None)
    email = models.EmailField("Email", max_length=320, blank=False, null=False, unique=True)
    password = models.CharField("Senha", max_length=240, editable=False)
    phone = models.CharField("Celular", max_length=15, null=True, default=None)
    attempts = models.PositiveSmallIntegerField(
        "Tentativas", default=0,
        help_text="Tentativas de login com a senha incorreta. "
        "Caso ultrapasse o limite definido nas configurações o usuário precisará redefini-la"
    )

    is_staff = models.BooleanField(
        "Administrador", default=False,
        help_text="Define se o usuário pode acessar o site Administrativo."
    )
    is_superuser = models.BooleanField(
        "Superusuário", default=False, editable=False,
        help_text="Define se o usuário possui todas as permissões. "
    )
    is_active = models.BooleanField(
        "Ativo", default=True,
        help_text="Define se o usuáruio deveria ser tratado como ativo. "
        "Desmarque ao invés de excluir contas."
    )

    date_joined = models.DateTimeField("Entrou em", default=timezone.now)
    last_login = models.DateTimeField("Último Login", blank=True, null=True, default=None)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "password"]

    CUSTOMER_ROLE = 1
    CUSTOMER_PREMIUM_ROLE = 2

    def __str__(self) -> str:
        return self.get_username()

    def get_name(self) -> str:
        return self.get_full_name().replace("None", "") 
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'usuario_users'