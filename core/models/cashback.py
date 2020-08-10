from django.db import models


class CashbackRange(models.Model):
    min = models.DecimalField("Valor Mínimo", default=0, max_digits=19, decimal_places=2)
    max = models.DecimalField("Valor Máximo", default=0, max_digits=19, decimal_places=2)
    percentage = models.DecimalField("Percentual",default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.min} - {self.max} - {self.percentage}'

    class Meta:
        verbose_name = 'Range'
        ordering = ['min']


class CachbackPurchase(models.Model):
    purchase = models.OneToOneField('Purchase', models.PROTECT, related_name='cashback')
    cashback_percentage = models.DecimalField('Percentual do cashback', max_digits=12, decimal_places=2, default=0)
    cashback_value = models.DecimalField(verbose_name='Valor do Cashback', max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.purchase}'

    class Meta:
        verbose_name = 'Cashback Compra'
