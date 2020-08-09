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
