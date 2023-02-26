from celery import shared_task
from django.core.mail import EmailMessage
from notification.models import Notification
import logging

logger = logging.getLogger(__name__)


email='operation@enclopediai-info.com'

@shared_task
def order_completed_notification(instance):
    try:
        title = '注文した商品のお支払いが完了しました。'
        body = '{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
            \n注文したアイテム{item}のお支払いが完了しました。\
            \n購入したアイテムに関してまして返却は必要ありませんのでそのままご利用いただけます。'.format(first_name=instance.user.first_name, last_name=instance.user.last_name, item=instance.reservation_item.product.product_name)
        Notification.objects.create(
            user=instance.user,
            title=title,
            body=body
        )
        msg = EmailMessage(
            from_email=email,
            to=[instance.user.email]
        )
        msg.tempalte_id='d-c8278c649a7047f28c6dc7e6eecb44f7'
        msg.dynamic_template_data = {
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
            "item": instance.reservation_item.product.product_name,
            "img": instance.reservation_item.product.img
        }
        msg.send(fail_silently=False)
    except:
        logging.error('注文した商品に関する通知に失敗しました。')
        pass

@shared_task
def order_canceled_notification(instance):
    try:
        title = '注文した商品のお支払いが失敗しました。'
        body = '{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
            \n注文したアイテムのお支払いに失敗しまたし。\
            \n現在ご登録いただいているお支払い情報に請求を行うことができませんでした。\
            お手数をおかけしますが現在登録いただいているお支払い情報をアカウントの管理から\
            更新くださいますよう、よろしくお願いいたします。'.format(first_name=instance.user.first_name, last_name=instance.user.last_name)
        Notification.objects.create(
            user=instance.user,
            title=title,
            body=body
        )
        msg = EmailMessage(
            from_email=email,
            to=[instance.user.email]
        )
        msg.tempalte_id='d-5418a157f4a94645a8f71ffb8926da65'
        msg.dynamic_template_data = {
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
        }
        msg.send(fail_silently=False)
    except:
        logging.error('注文した商品に関する通知に失敗しました。')
        pass
