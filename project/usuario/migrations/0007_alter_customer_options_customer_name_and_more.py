# Generated by Django 4.2.4 on 2023-11-17 01:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_unit_options'),
        ('usuario', '0006_payment_date_time'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': [('payments', 'Can view self payments'), ('favorites', 'Can view favorites'), ('buy_in_term', 'Can buy in term')], 'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(default='nome', max_length=100, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='bill',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Conta'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='unit_favorite', to='produto.unit', verbose_name='Favoritos'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='limit',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Define o valor máximo da conta à prazo. Deixe vazio caso indefinido.', max_digits=5, verbose_name='Limite'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='user_customer', to='usuario.customer', verbose_name='Cliente'),
        ),
    ]