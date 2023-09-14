# Generated by Django 4.2.4 on 2023-09-02 20:31

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produto', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Primeiro Nome')),
                ('last_name', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Último Nome')),
                ('email', models.EmailField(max_length=320, unique=True, verbose_name='Email')),
                ('password', models.CharField(max_length=240, editable=False, verbose_name='Senha')),
                ('phone', models.CharField(max_length=14, verbose_name='Celular')),
                ('attempts', models.PositiveSmallIntegerField(default=0, help_text='Tentativas de login com a senha incorreta. Caso ultrapasse o limite definido nas configurações o usuário precisará redefini-la', verbose_name='Tentativas')),
                ('is_staff', models.BooleanField(default=False, help_text='Define se o usuário pode acessar o site Administrativo.', verbose_name='Administrador')),
                ('is_superuser', models.BooleanField(default=False, editable=False, help_text='Define se o usuário possui todas as permissões. ', verbose_name='Superusuário')),
                ('is_active', models.BooleanField(default=True, help_text='Define se o usuáruio deveria ser tratado como ativo. Desmarque ao invés de excluir contas.', verbose_name='Ativo')),
                ('date_joined', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Entrou em')),
                ('last_login', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Último Login')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
                'db_table': 'usuario_users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=5, null=True, verbose_name='Conta')),
                ('limit', models.DecimalField(blank=True, decimal_places=2, default=None, help_text='Define o valor máximo da conta à prazo. Deixe vazio caso indefinido.', max_digits=5, null=True, verbose_name='Limite')),
                ('default', models.BooleanField(default=True, verbose_name='Perfil Padrão')),
                ('favorites', models.ManyToManyField(blank=True, to='produto.unit', verbose_name='Favoritos')),
                ('user', models.OneToOneField(blank=True, db_column='user_id', default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'usuario_customers',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Quantia')),
                ('method', models.CharField(choices=[('M', 'Dinheiro'), ('P', 'Pix')], default='P', max_length=1, verbose_name='Método')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='usuario.customer', verbose_name='Ciente')),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
                'db_table': 'usuario_payments',
            },
        ),
    ]
