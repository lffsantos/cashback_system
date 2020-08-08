# Generated by Django 3.1 on 2020-08-08 21:01

import core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashBackUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that e-mail already exists.'}, max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(blank=True, max_length=60, verbose_name='Username')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('cashbackuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.cashbackuser')),
                ('cpf', models.CharField(max_length=11, unique=True, validators=[core.validators.validate_cpf], verbose_name='CPF')),
                ('name', models.CharField(max_length=200, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Revendedor',
                'verbose_name_plural': 'Revendedores',
            },
            bases=('core.cashbackuser',),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_code', models.CharField(max_length=100, unique=True, verbose_name='Código da Compra')),
                ('value', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Valor da Compra')),
                ('status', models.CharField(choices=[('in_validation', 'Em validação'), ('approve', 'Aprovado')], default='in_validation', max_length=20)),
                ('purchase_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purcharse', to='core.dealer')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
            },
        ),
    ]