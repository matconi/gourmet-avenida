# Generated by Django 4.2.4 on 2023-11-23 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_unit_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategory_of',
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(editable=False, max_length=120),
        ),
    ]
