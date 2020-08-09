import datetime

from django.db import models
from django.utils import timezone


class Purchase(models.Model):
    IN_VALIDATION = 'in_validation'
    APRROVED = 'approved'
    STATUS_CHOICES = [
        (IN_VALIDATION, 'Em validação'),
        (APRROVED, 'Aprovado'),
    ]
    dealer = models.ForeignKey('Dealer', on_delete=models.PROTECT, related_name="purchase")
    purchase_code = models.CharField('Código da Compra', max_length=100)

    value = models.DecimalField('Valor da Compra', max_digits=19, decimal_places=2, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=IN_VALIDATION,)
    purchase_at = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    cashback_percentage = models.DecimalField('Percentual do cashback', max_digits=12, decimal_places=2, default=0)
    cashback_value = models.DecimalField(verbose_name='Valor do Cashback', max_digits=12, decimal_places=2, default=0)

    @staticmethod
    def get_cashback(value):
        from core.models import CashbackRange
        range = CashbackRange.objects.filter(min__lt=value).last()
        if not range:
            return 0, 0

        percentage = range.percentage
        value = (value * percentage) / 100
        return percentage, value

    def save(self, *args, **kwargs):
        self.cashback_percentage, self.cashback_value = Purchase.get_cashback(self.value)
        super(Purchase, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.purchase_code}'

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['purchase_at']
