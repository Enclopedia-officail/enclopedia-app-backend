from django.db.models.signals import pre_save
from django.dispatch import receiver
from .tasks import order_completed_notification, order_canceled_notification
from .models import Order
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Order)
def updated_order(sender, instance, update_fields, *args, **kwargs):
    if ("status" in list(update_fields)):
        if instance.status == 'completed':
            order_completed_notification(instance)
        elif instance.status == 'cancelled':
            order_canceled_notification(instance)
        else:
            logger.info('orderモデルのupdate_fieldsが存在しません。')
    else:
        logger.error('商品購入に関する通知が失敗しました。')