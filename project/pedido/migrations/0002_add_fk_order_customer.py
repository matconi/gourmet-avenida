# Generated by Django 4.2.4 on 2023-09-02 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pedido', '0001_initial'),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(db_column='customer_id', on_delete=django.db.models.deletion.RESTRICT, to='usuario.customer', verbose_name='Cliente'),
        ),
    ]
