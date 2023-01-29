from django.db.models.signals import pre_save
from django.dispatch import receiver
from .tasks import create_register_subscription_notification, update_subscriptoin_notification, cancel_subscription_notification

from subscription.models import StripeAccount
import logging
logger = logging.getLogger(__name__)

#subscription登録時にこちらのemailアドレスを送信するようにする
@receiver(pre_save, sender=StripeAccount)
def send_subscription_register_email(sender, instance, update_fields, *args, **kwargs):
    try:
        if ("start_date" in list(update_fields)):
            create_register_subscription_notification(instance)
        else:
            pass
    except:
        logger.error('サブスクリプション登録通知 user:{} emailが送信できませんでした'.format(instance.user_id.id))
        pass

#subscription更新時にこちらのemailを送信"
@receiver(pre_save, sender=StripeAccount)
def send_subscription_update_email(sender, instance, update_fields, *args, **kwargs):
    try:
        if("update_date" in list(update_fields)):
            print('start')
            update_subscriptoin_notification(instance)
        else:
            pass
    except:
        logger.error('サブスクリプション更新通知 user:{} emailが送信できませんでした'.format(instance.user_id.id))
        pass

#subscription登録解約時にもmailmessageを送信
@receiver(pre_save, sender=StripeAccount)
def send_subscription_cancel_email(sender, instance, update_fields, *args, **kwargs):
    #解約後にすぐに無効化はしない
    try:
        print('delete')
        if ("cancel_date" in list(update_fields)):
            cancel_subscription_notification(instance)
        else:
            pass
    except:
        logger.error('サブスクリプション解約通知 user:{} emailが送信できませんでした')
        pass
