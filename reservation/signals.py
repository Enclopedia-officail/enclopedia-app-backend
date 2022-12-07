from django.db.models.signals import pre_save
from django.dispatch import receiver
from .task import create_reservation_notification
from .models import Reservation
import logging
logger = logging.getLogger(__name__)
# 予約回数を制限するためのsignal
#email送信とカラム作成でuserに遅延が起きないようにする必要がある
@receiver(pre_save, sender=Reservation)
def shinnping_notification(sender, instance, update_fields, *args, **kwargs):
    try:
        if("shipping_number" in list(update_fields) & instance.status == 3):
            pass
        else:
            pass
    except:
        logger.error('予約番号[{}]: 発送通知の送信に失敗しました'.format(instance.id))

import task
@receiver(pre_save, sender=Reservation)
def reservation_notification(sender, instance, update_fileds, *args, **kwargs):
    try:
        if("status" in list(update_fileds)):
            if instance.status == 1:
                task.create_reservation_success_notification(instance)
            elif instance.status == 2:
                task.create_reservation_failed_notification(instance)
            elif instance.status == 3:
                task.shipping_product_notification(instance)
            elif instance.status == 4:
                task.return_product_notification(instance)
            elif instance.status == 5:
                task.return_product_success_notification(instance)
                task.return_favorite_product_notification(instance)
    except:
        logger.error('notification通知に失敗しました。')