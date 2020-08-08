from django.db import models
from django.utils import timezone


class Purchase(models.Model):
    IN_VALIDATION = 'in_validation'
    APRROVED = 'approve'
    STATUS_CHOICES = [
        (IN_VALIDATION, 'Em validação'),
        (APRROVED, 'Aprovado'),
    ]
    dealer = models.ForeignKey('Dealer', on_delete=models.PROTECT, related_name="purcharse")
    purchase_code = models.CharField('Código da Compra', max_length=100, unique=True, null=False)

    value = models.DecimalField('Valor da Compra', max_digits=19, decimal_places=2, null=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=IN_VALIDATION,
    )
    purchase_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    @property
    def cpf(self):
        return self.dealer.cpf

    def __str__(self):
        return f'{self.purchase_code}'

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
