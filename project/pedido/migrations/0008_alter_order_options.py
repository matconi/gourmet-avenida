# Generated by Django 4.2.7 on 2023-12-20 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0007_alter_order_options_order_discount_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date_time'], 'permissions': [('self_orders', 'Can view self orders'), ('cancel_book', 'Can cancel booking')], 'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
    ]
