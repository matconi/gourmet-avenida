# Generated by Django 4.2.4 on 2023-09-02 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('slug', models.SlugField(max_length=120, verbose_name='Link')),
                ('subcategory_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='produto.category', verbose_name='Subcategoria de ')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'produto_categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('description', models.CharField(max_length=400, verbose_name='Descrição')),
                ('slug', models.SlugField(max_length=120, verbose_name='Link')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='produto.category', verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'db_table': 'produto_products',
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Variante',
                'verbose_name_plural': 'Variantes',
                'db_table': 'produto_variants',
            },
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='produto.variant', verbose_name='Variante')),
            ],
            options={
                'verbose_name': 'Variação',
                'verbose_name_plural': 'Variações',
                'db_table': 'produto_variations',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('sku', models.CharField(max_length=12, unique=True, verbose_name='Código')),
                ('image', models.ImageField(upload_to='produtos', verbose_name='Imagem')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Preço')),
                ('promotional', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Preço promocional')),
                ('stock', models.PositiveIntegerField(verbose_name='Estoque')),
                ('booked', models.PositiveIntegerField(default=0, verbose_name='Reservado')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='produto.product', verbose_name='Produto')),
                ('variations', models.ManyToManyField(blank=True, related_name='variations_units', to='produto.variation')),
            ],
            options={
                'verbose_name': 'Unidade',
                'verbose_name_plural': 'Unidades',
                'db_table': 'produto_units',
            },
        ),
    ]
