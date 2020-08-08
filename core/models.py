from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone

from core.validators import validate_cpf


class Dealer(models.Model):
    IN_VALIDATION = 'in_validation'
    APRROVED = 'approve'
    STATUS_CHOICES = [
        (IN_VALIDATION, 'Em validação'),
        (APRROVED, 'Aprovado'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField('CPF', max_length=11, unique=True, validators=[validate_cpf], null=False, blank=False)
    email = models.EmailField(
        "Email",
        error_messages={
            'unique': "Revendedor com esse email já existe.",
        },
        blank=False,
        null=False,
        unique=True)

    name = models.CharField('Nome', max_length=200, null=False, blank=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=IN_VALIDATION,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Revendedor'
        verbose_name_plural = 'Revendedores'


class Purchase(models.Model):
    purchase_code = models.CharField('Código da Compra', max_length=100, unique=True, null=False)
    value = models.DecimalField('Valor da Compra', max_digits=19, decimal_places=2, null=False)
    purchase_at = models.DateTimeField(default=timezone.now)
    dealer = models.ForeignKey('Dealer', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.purchase_code}'

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
