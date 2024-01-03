# Generated by Django 4.2.7 on 2023-12-31 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderunit',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=5.0, max_digits=6, verbose_name='Preço'),
            preserve_default=False,
        ),
    ]