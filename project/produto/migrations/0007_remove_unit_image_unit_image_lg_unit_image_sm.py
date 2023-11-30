# Generated by Django 4.2.7 on 2023-11-28 15:57

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_alter_category_slug_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='image',
        ),
        migrations.AddField(
            model_name='unit',
            name='image_lg',
            field=django_resized.forms.ResizedImageField(crop=None, default='', force_format='JPEG', keep_meta=True, quality=75, scale=1, size=[512, 512], upload_to='produtos/lg', verbose_name='Imagem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unit',
            name='image_sm',
            field=django_resized.forms.ResizedImageField(crop=None, default='', editable=False, force_format='JPEG', keep_meta=True, quality=75, scale=1, size=[256, 256], upload_to='produtos/sm', verbose_name='Imagem'),
            preserve_default=False,
        ),
    ]