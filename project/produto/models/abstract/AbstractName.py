from django.db import models

class AbstractName(models.Model):
    name = models.CharField("Nome", max_length=100)

    class Meta:
        abstract = True