from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Reservation
from . import task
import logging
logger = logging.getLogger(__name__)
# 予約回数を制限するためのsignal
#email送信とカラム作成でuserに遅延が起きないようにする必要がある
@receiver(pre_save, sender=Reservation)
def reservation_notification(sender, instance, update_fields, *args, **kwargs):
    try:
        if("status" in list(update_fields)):
            print("start")
            print(instance.status)
            if int(instance.status) == 1:
                task.create_reservation_success_notification(instance)
            elif int(instance.status) == 2:
                task.create_reservation_failed_notification(instance)
            elif int(instance.status) == 3:
                task.shipping_product_notification(instance)
            elif int(instance.status) == 4:
                task.return_product_notification(instance)
            elif int(instance.status) == 5:
                task.return_product_success_notification(instance)
                task.return_favorite_product_notification(instance)
            else:
                print('end')
    except:
        logger.error('notification通知に失敗しました。')