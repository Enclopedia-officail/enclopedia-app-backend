from django.db.models.signals import pre_save
from django.dispatch import receiver
from .task import create_reservation_notification
from .models import Reservation
import logging
logger = logging.getLogger(__name__)
# 予約回数を制限するためのsignal
#email送信とカラム作成でuserに遅延が起きないようにする必要がある
@receiver(pre_save, sender=Reservation)
def notification_create(sender, instance, update_fields, *args, **kwargs):
    try:
        if ("status" in list(update_fields)):
            print('start')
            create_reservation_notification(instance)
        else:
            pass
    except:
        logger.error('予約番号[{}]:確認用emailが送信できませんでした'.format(instance.id))
        pass

@receiver(pre_save, sender=Reservation)
def shinnping_notification(sender, instance, update_fields, *args, **kwargs):
    try:
        if("shipping_number" in list(update_fields) & instance.status == 3):
            pass
        else:
            pass
    except:
        logger.error('予約番号[{}]: 発送通知の送信に失敗しました'.format(instance.id))
            