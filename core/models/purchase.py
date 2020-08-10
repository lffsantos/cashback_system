import datetime

from django.db import models


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

    def __str__(self):
        return f'{self.purchase_code} - {self.get_status_display()}'

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['purchase_at']
