# coding: utf-8
import logging

from django.db.models import Sum
from django.utils import timezone

logger = logging.getLogger(__name__)


def get_percent_cashback(value):
    from core.models import CashbackRange
    range = CashbackRange.objects.filter(min__lt=value).last()
    if not range:
        return 0

    percentage = range.percentage
    return percentage


def update_cashback_dealer_handler(sender, instance, created, **kwargs):
    from core.models import Purchase, CachbackPurcharse
    actual_date = timezone.now()
    year, month = actual_date.year, actual_date.month
    purcharses = Purchase.objects.filter(dealer=instance.dealer, purchase_at__month=month, purchase_at__year=year)
    value = purcharses.aggregate(Sum('value')).get('value__sum')
    cashback_percent = get_percent_cashback(value)
    for p in purcharses:
        CachbackPurcharse.objects.update_or_create(
            purcharse=p,
            defaults={
                "cashback_percentage": cashback_percent,
                "cashback_value": (p.value * cashback_percent) / 100
            }
        )
