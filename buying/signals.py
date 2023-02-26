from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .tasks import order_completed_notification, order_canceled_notification
from .models import Order, OrderItem
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrderItem)
def create_order_item(sender, instance, created, **kwargs):
    if created:
        order_completed_notification(instance)
    else:
        pass

@receiver(pre_save, sender=Order)
def updated_order(sender, instance, update_fields, *args, **kwargs):
    if update_fields is None:
        pass
    else:
        if ("status" in list(update_fields)):
            if instance.status == 'cancelled':
                order_canceled_notification(instance)
            else:
                pass
        else:
            logger.error('商品購入に関する通知が失敗しました。')
            pass