# Generated by Django 4.2.7 on 2023-12-26 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0010_alter_variety_options_alter_variation_variety'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='promotional',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Preço acima do original que mostrará riscado.', max_digits=6, null=True, verbose_name='Preço promocional'),
        ),
    ]
