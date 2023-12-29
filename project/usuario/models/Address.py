
from django.db import models

class Address(models.Model):
    class State(models.TextChoices):
        ACRE = ('AC', 'Acre',)
        ALAGOAS = ('AL', 'Alagoas',)
        AMAPA = ('AP', 'Amapá',)
        AMAZONAS = ('AM', 'Amazonas',)
        BAHIA = ('BA', 'Bahia',)
        CEARA = ('CE', 'Ceará',)
        ESPIRITO_SANTO = ('ES', 'Espírito Santo',)
        GOIAS = ('GO', 'Goiás',)
        MARANHAO = ('MA', 'Maranhão',)
        MATO_GROSSO = ('MT', 'Mato Grosso',)
        MATO_GROSSO_DO_SUL = ('MS', 'Mato Grosso do Sul',)
        MINAS_GERAIS = ('MG', 'Minas Gerais',)
        PARA = ('PA', 'Pará',)
        PARAIBA = ('PB', 'Paraíba',)
        PARANA = ('PR', 'Paraná',)
        PERNAMBUCO = ('PE', 'Pernambuco',)
        PERNAMBUCO = ('PE', 'Pernambuco',)
        PIAUI = ('PI', 'Piauí',)
        RIO_DE_JANEIRO = ('PJ', 'Rio de Janeiro',)
        RIO_GRANDE_DO_NORTE = ('RN', 'Rio Grande do Norte',)
        RIO_GRANDE_DO_SUL = ('RS', 'Rio Grande do Sul',)
        RONDONIA = ('RO', 'Rondonia',)
        RORAIMA = ('RR', 'Roraima',)
        SANTA_CATARINA = ('SC', 'Santa Catarina',)
        SAO_PAULO = ('SP', 'São Paulo',)
        SERGIPE = ('SE', 'Sergipe',)
        TOCANTINS = ('TO', 'Tocantins',)

    cep = models.CharField("CEP", max_length=9)
    street = models.CharField("Rua", max_length=150)
    number = models.PositiveSmallIntegerField("Número")
    complement = models.CharField("Complemento", max_length=60, blank=True, null=True, default=None)
    city = models.CharField("Cidade", max_length=100)
    state = models.CharField("Estado", max_length=2, default=State.MINAS_GERAIS)

    customer = models.ForeignKey("Customer", on_delete=models.RESTRICT,
        verbose_name='Cliente'
    )

    def __str__(self) -> str:
        return self.street

    class Meta:
        abstract = True
        # verbose_name = 'Endereço'
        # verbose_name_plural = 'Endereços'
        # db_table = 'usuario_addresses'