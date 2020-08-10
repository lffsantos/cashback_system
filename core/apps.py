from django.apps import AppConfig
from django.db.models.signals import post_save

# from core.receivers import update_cashback_dealer_handler


class CoreConfig(AppConfig):
    name = 'core'

    # def ready(self):
    #     from core.models import Purchase
    #     post_save.connect(update_cashback_dealer_handler, sender=Purchase)
