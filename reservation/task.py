from celery import shared_task
from notification.models import Notification
from account_history.models import Favorite
from .models import ReservationItem
from .serializers import ReservationItemSerializer
from django.conf import settings
from django.core.mail import EmailMessage

import logging
logger = logging.getLogger(__name__)


#reservation登録が成功した場合と失敗場合の処理をする
email = 'operation@enclopediai-info.com'

#exceptでpassにしてあるがloggerでerror logを記録できるようにする

@shared_task
def create_reservation_success_notification(instance):
    try:
        title='商品の予約が完了しました'
        body='{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
            \n商品の予約が完了しました、発送まで2日程度のお時間を頂いております。商品の到着まで今しばらくお待ち頂けますよう願います。'.format(first_name=instance.user.first_name, last_name=instance.user.last_name)
        Notification.objects.create(
            user=instance.user,
            title=title,
            body=body
        )
        msg = EmailMessage(
            from_email=email,
            to=[instance.user.email]
        )
        reservations = ReservationItem.objects.select_related('product', 'reservation').filter(reservation=instance)
        serializer = ReservationItemSerializer(reservations, many=True)
        msg.template_id="d-d2348fb0b82847358b37250e34822cf4"
        msg.dynamic_template_data = {
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
            "items": serializer.data
        }
        msg.send(fail_silently=False)
    except:
        logger.error('レンタル完了通知 user:{} に通知失敗'.format(instance.user.id))
        pass

@shared_task
def create_reservation_failed_notification(instance):
    try:
        title='商品の予約が失敗しました。'
        body='{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
            \n商品の予約に失敗しました、貸出中アイテムがある場合は予約をすることができません。\
            現在貸出中のアイテムがあるか確認を行なって下さい、\
            貸出中のアイテムがない場合には運営までご連絡頂けますようよろしくお願い致します。'.format(first_name=instance.user.first_name, last_name=instance.user.last_name)
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
        }
        msg.send(fail_silently=False)
    except:
        logger.info('予約受付失敗 user:{} に通知失敗'.format(instance.user.id))
        pass

@shared_task
def shipping_product_notification(instance):
    try:
        title='Enclopediaからの発送が完了しました。'
        body='{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
            発送が完了いたしました、商品到着までの間もうしばらくお待ち下さい。'.format(first_name=instance.user.first_name, last_name=instance.user.last_name)
        Notification.objects.create(
            user=instance.user,
            title=title,
            body=body
        )
        reservation_items = ReservationItem.objects.select_related('product', 'reservation').filter(reservation=instance)
        serializer = ReservationItemSerializer(reservation_items, many=True)
        msg = EmailMessage(
            from_email=email,
            to=[instance.user.email]
        )
        msg.template_id='d-ee461e835eab4d51ad803cdf2f53055c'
        msg.dynamic_template_data = {
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'items': serializer.data
        }
        msg.send(fail_silently=False)
    except:
        logger.error('商品発送通知　user:{}に通知失敗').format(instance.user.id)

@shared_task
def return_product_notification(instance):
    try:
        title='商品返却発送手続きが完了しました。'
        body='{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
            Enclopedia運営に商品が到着し問題がございませんでしたら次の商品をレンタルすることができます、確認までの間少々お時間いただきますことご了承ください。'.format(first_name=instance.user.first_name, last_name=instance.user.last_name)
        Notification.objects.create(
            user=instance.user,
            title=title,
            body=body
        )
        msg = EmailMessage(
            from_email=email,
            to=[instance.user.email]
        )
        msg.template_id='d-4a4aa932361948579c66aa19a580590e'
        msg.dynamic_template_data = {
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
        }
        msg.send(fail_silently=False)
    except:
        logger.error('商品返却開始通知 user:{}に通知失敗'.format(instance.user.id))
        pass

@shared_task
def return_product_success_notification(instance):
    try:
        title='商品の返却が完了しました'
        body='{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスのご利用ありがとうございます。\
            返却して頂いた商品の確認が取れましたので商品のレンタルが可能となりました。またのご利用お待ちしております。'.format(first_name=instance.user.first_name, last_name=instance.user.last_name)
        Notification.objects.create(
            user=instance.user,
            title=title,
            body=body
        )
        msg = EmailMessage(
            from_email=email,
            to=[instance.user.email]
        )
        msg.template_id='d-edcbef5a2982462aa1ab101e1b81da28'
        msg.dynamic_template_data = {
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
        }
        msg.send(fail_silently=False)
    except:
        logger.error('商品返却完了通知 user:{}に通知失敗'.format(instance.user.id))
        pass

#お気に入りに登録した商品で返却通知を行うための処理
@shared_task
def return_favorite_product_notification(instance):
    try:
        reservation_items = ReservationItem.objects.select_related('product', 'reservation').filter(reservation=instance)
        for item in reservation_items:
            favorites = Favorite.objects.select_related('user', 'product').filter(product=item.product)
            for favorite in favorites:
                if favorite.is_notification:
                    try:
                        title="お気に入りに登録した商品が返却されました"
                        body="{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
                            お気に入りにした商品が返却されました、早速ですが気になっている商品をレンタルしてみませんか？".format(first_name=favorite.user.first_name, last_name=favorite.user.last_name)
                        Notification.objects.create(
                            user=favorite.user,
                            title=title,
                            body=body
                        )

                        msg = EmailMessage(
                            from_email=email,
                            to=[favorite.user.email]
                        )
                        print(favorite.user.email)
                        msg.template_id="d-5b0f16837150416fa01a3027eefe2211"
                        msg.dynamic_template_data = {
                            "first_name": favorite.user.first_name,
                            "last_name": favorite.user.last_name,
                        }
                        msg.send(fail_silently=False)
                    except:
                        logger.error('お気に入り商品返却通知 user:{} 失敗'.format(favorite.user.id))
                        pass
    except:
        logger.error('お気に入り商品返却通知 user:{} 失敗'.format(favorite.user.id))
        pass


