from django.contrib.auth import get_user_model
from django.db import models

from core.validators import validate_cpf

User = get_user_model()


class DealerManager(models.Manager):
    def create_dealer(self, email, name, cpf, password):
        user = self.model(email=email, cpf=cpf, name= name)
        user.set_password(password)
        user.save()
        return user


class Dealer(User):
    cpf = models.CharField('CPF', max_length=11, unique=True, validators=[validate_cpf], null=False, blank=False)
    name = models.CharField('Nome Completo', max_length=200, null=False, blank=False)
    objects = DealerManager()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Revendedor'
        verbose_name_plural = 'Revendedores'
