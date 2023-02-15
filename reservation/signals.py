from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Reservation, ReservationItem
from notification.models import Todo
from . import task
import environ
import logging
logger = logging.getLogger(__name__)
# 予約回数を制限するためのsignal
#email送信とカラム作成でuserに遅延が起きないようにする必要がある

env = environ.Env()

class CreateReturnTodo():

    def __init__(self, user, title, thumbnail, url):
        self.user = user
        self.title = title
        self.thumbnail = thumbnail
        self.url = url
    
    def create(self):
        todo = Todo.objects.create(
            user = self.user,
            title = self.title,
            thumbnail = self.thumbnail,
            url = self.url
        )
        return todo 

@receiver(pre_save, sender=Reservation)
def reservation_notification(sender, instance, update_fields, *args, **kwargs):
    #signalに関してcatchするエラーを限定する必要がある
    try:
        if("status" in list(update_fields)):
            if int(instance.status) == 1:
                task.create_reservation_success_notification(instance)
            elif int(instance.status) == 2:
                task.create_reservation_failed_notification(instance)
            elif int(instance.status) == 3:
                task.return_product_todo(instance)
                task.shipping_product_notification(instance)
                #返却をやることリストに追加する処置を行う
            elif int(instance.status) == 4:
                task.return_product_notification(instance)
            elif int(instance.status) == 5:
                task.return_product_success_notification(instance)
                task.return_favorite_product_notification(instance)
            else:
                pass
        else:
            logger.info('statusの変更がありませんでした。')
            pass
    except:
        logger.error('notification通知に失敗しました。')
        pass

@receiver(pre_save, sender=ReservationItem)
def review_return_item(sender, instance, update_fields, *args, **kwargs):
    try:
        if("review" in list(update_fields)):
            task.return_product(instance)
        else:
            pass
    except:
        logger.error('ユーザの信用度評価の計算に失敗しました。')
        pass
            
