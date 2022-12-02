from celery import shared_task
from notification.models import Notification
from django.conf import settings
from django.core.mail import EmailMessage

import logging
logger = logging.getLogger(__name__)


#reservation登録が成功した場合と失敗場合の処理をする
email = 'operation@enclopediai-info.com'

#exceptでpassにしてあるがloggerでerror logを記録できるようにする
@shared_task
def create_reservation_notification(instance):
    #レンタル商品の登録が完了した場合はnotificationとemailで成功通知を行う
    if instance.status == 1:
        logging.info('レンタル完了通知 user:{} に通知'.format(instance.user.id))
        try:
            title='商品の予約が完了しました'
            body='商品の予約が完了しました、発送まで3日程度を有しております。商品の到着まで今しばらくお待ち頂けますよう願います。'
            Notification.objects.create(
                user=instance.user,
                title='商品の予約が完了しました',
                body='商品の予約が完了しました、発送まで3日程度を有しております。商品の到着まで今しばらくお待ち頂けますよう願います。'
            )
            msg = EmailMessage(
                from_email=email,
                to=[instance.user.email]
            )
            msg.template_id="d-d2348fb0b82847358b37250e34822cf4"
            msg.dynamic_template_data = {
                "first_name": instance.user.first_name,
                "last_name": instance.user.last_name,
            }
            msg.send(fail_silently=False)
        except:
            logger.error('レンタル完了通知 user:{} に通知失敗'.format(instance.user.id))
            pass
    #予約が受け付けられなかった場合の処理を行う
    #商品の予約が失敗した場合には
    elif instance.status == 2:
        try:
            title='商品の予約が失敗しました。'
            body='商品の予約に失敗しました、貸出中アイテムがある場合は予約をすることができません。現在貸出中のアイテムがあるか確認を行なって下さい、貸出中のアイテムがない場合には運営までご連絡頂けますようよろしくお願い致します。'
            Notification.objects.create(
                user=instance.user,
                title=title,
                body=body,
                url='http://enclopedia.co.jp'
            )
            msg = EmailMessage(
                from_email=email,
                to=[instance.user.email]
            )
            msg.template_id=''
            msg.dynamic_template_data = {
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'title':title,
                'body':body
            }
            msg.send(fail_silently=False)
        except:
            logger.info('予約受付失敗 user:{} に通知失敗'.format(instance.user.id))
            pass
    #商品を発送した場合の処理
    elif instance.status == 3:
        try:
            title='Enclopediaからの発送が完了しました。'
            body='発送が完了いたしました、商品到着までの間もうしばらくお待ち下さい。'
            Notification.objects.create(
                title=title,
                body=body
            )
            msg = EmailMessage(
                from_email=email,
                to=[instance.user.email]
            )
            msg.template_id=''
            msg.dynamic_template_data = {
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'title': title,
                'body': body
            }
            msg.send(fail_silently=False)
        except:
            logger.error('商品発送通知　user:{}に通知失敗').format(instance.user.id)
            pass
    #商品の返却手続きの完了
    elif instance.status == 4:
        try:
            title='お客様の返却発送手続きが完了しました。'
            body='商品返却に運営が確認でき次第予約を再開することができます、確認までの間少々お待ち下さい。'
            Notification.objects.create(
                title=title,
                body=body
            )
            msg = EmailMessage(
                from_email=email,
                to=[instance.user.email]
            )
            msg.template_id=''
            msg.dynamic_template_data = {
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'title': title,
                'body':body
            }
            msg.send(fail_silently=False)
        except:
            logger.error('商品返却開始通知 user:{}に通知失敗'.format(instance.user.id))
            pass
    elif instance.status == 5:
        try:
            title='商品の返却が完了しました'
            body='この度はEnclopediaファッションレンタルサービスのご利用ありがとうございます、無事商品の返却が完了致したした。商品の予約が可能となりました、またのご利用お待ちしております。'
            Notification.objects.craete(
                title=title,
                body=body
            )
            msg = EmailMessage(
                from_email=email,
                to=[instance.user.email]
            )
            msg.template_id=''
            msg.dynamice_template_data = {
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'title': title,
                'body': body
            }
            msg.send(fail_silently=False)
        except:
            logger.error('商品返却完了通知 user:{}に通知失敗'.format(instance.user.id))
            pass
    else:
        logger.error('reservation statusが見つかりませんでした')
        pass