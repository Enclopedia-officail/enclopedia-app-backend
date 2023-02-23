from celery import shared_task
from django.core.mail import EmailMessage
from .models import StripeAccount
from notification.models import Notification
from django.conf import settings
import environ
import logging
import os


logger = logging.getLogger(__name__)
env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))

#subscription登録時にこちらのメールに送信する
#reservation から取得したitemを
email = 'operation@enclopediai-info.com'

@shared_task
def create_register_subscription_notification(instance):
    #サブスクリプションの登録を行った際の処理
    try:
        title = 'サブスクリプションの登録が完了しました'
        body='{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
        \nサブスクリプション{plan}プランへの登録が完了しました.\
        \n早速商品をレンタルすることができます、引き続きEcnlopediaファッションレンタルサービスをお楽しみください。'.format(first_name=instance.user_id.first_name, last_name=instance.user_id.last_name, plan=instance.plan)
        Notification.objects.create(
            user=instance.user_id,
            title=title,
            body=body
        )
        msg = EmailMessage(
            from_email=email,
            to=[instance.user_id.email]
        )
        msg.template_id='d-0cad5a0123fc4aa48a74cac49e7c9993'
        msg.dynamic_template_data = {
            "first_name": instance.user_id.first_name,
            "last_name": instance.user_id.last_name,
            "plan": instance.plan
        }
        msg.send(fail_silently=False)
    except:
        logging.info('サブスクリプション登録完了通知 user:{}に通知失敗'.format(instance.user_id.id))
        pass

@shared_task
def cancel_subscription_notification(instance):
    #サブスクリプションの解約を行なった際に送信する
    try:
        cancel_date=instance.cancel_date.strftime('%Y年%m月%d日')
        title='サブスクリプションの解約が完了しました'
        body='{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。 \
            \n{plan}プランの解約が完了しました。\
            \n解約後ご利用のプランに関しましては{cancel_date}までご利用いただけます。\
            \n引き続きEnclopediaファッションレンタルサービスをよろしくお願い致します。'.format(first_name=instance.user_id.first_name, last_name=instance.user_id.last_name, plan=instance.plan, cancel_date=cancel_date)
        Notification.objects.create(
            user=instance.user_id,
            title=title,
            body=body
        )
        msg = EmailMessage(
            from_email=email,
            to=[instance.user_id.email]
        )
        msg.template_id='d-57e16e789a3d408a8b65230191a36a0d'
        msg.dynamic_template_date = {
            'first_name': instance.user_id.first_name,
            'last_name': instance.user_id.last_name,
            'created_at': cancel_date,
            'plan': instance.plan
        }
        msg.send(fail_silently=False)
    except:
        logging.info('サブスクリプション更新完了通知 user:{}に通知失敗'.format(instance.user_id.id))
        pass

#サブスクリプションの更新をおこなう
@shared_task
def update_subscriptoin_notification(instance):
    try:
        update_date = instance.update_date.strftime('%Y年%m月%d日')
        title='サブスクリプションプランの変更が完了しました'
        body='{first_name}{last_name}様Enclopediaファッションレンタルサービスをご利用頂きありがとうございます。\
            \n{plan}プランへの変更が完了しました,次回更新日は{update_date}となります。\
            \n引き続きEnclopediaファッションレンタルサービスをよろしくお願いします。'.format(first_name=instance.user_id.first_name, last_name=instance.user_id.last_name, plan=instance.plan, update_date=update_date)
        Notification.objects.create(
            user=instance.user_id,
            title=title,
            body=body
        )
        msg = EmailMessage(
            from_email=email,
            to=[instance.user_id.email]
        )
        msg.template_id="d-79949eb6e02848d18750dd36bf63654e"
        msg.dynamic_template_data = {
            'first_name': instance.user_id.first_name,
            'last_name': instance.user_id.last_name,
            'plan': instance.plan,
            'update_date': update_date
        }
        msg.send(fail_silently=False)
    except:
        logging.info('サブスクリプション削除完了通知 user:{}に通知失敗'.format(instance.user_id.id))
        pass

@shared_task
def update_subscription_payment_fail_notification(instance):
    #サブスクリプション更新料の支払いに失敗
    try:
        Notification.objects.create(
            user=instance.user_id,
            title="サブスクリプション更新料金の支払いに失敗しました",
            body="{first_name}{last_name}Enclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
                \nサブスクリプション更新料金の支払いに失敗しました。\
                \nお支払いが完了するまで一時的に商品のレンタルをすることができなくなりますのでご了承ください。"
        ).format(first_name=instance.user_id.first_nmae, last_name=instance.user_id.last_name)

        msg = EmailMessage(
            from_email="operation@enclopediai-info.com",
            to=[instance.user_id.email]
        )
        msg.template_id="d-215f2c14ea9943a2bddced9f5e123f46"
        msg.dynamic_template_date = {
            'frist_name': instance.user_id.first_name,
            'last_name': instance.user_id.last_name,
        }
        msg.send(fail_silently=False)
    except:
        logging.info('サブスクリプション更新料金催促通知 user:{} に通知失敗'.format(instance.user_id.id))


@shared_task
def subscription_update_confirmation_notification(instance):
#サブスクリプション更新日から一週間前の通知
    Notification.objects.create(
        user=instance.user_id,
        title="サブスクリプション更新期日の数日前となりました。",
        body="{first_name}{last_name}Enclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
            \nサブスクリプション更新期日の数日前となりました。詳細に関してましてはアカウント管理画面のサブスクリプションからご確認ください。\
            \n今後ともEnclopediaファッションレンタルサービスをよろしくお願い致します。".format(first_name=instance.user_id.first_name, last_name=instance.user_id.last_name)
    )
    msg = EmailMessage(
        from_email="operation@enclopediai-info.com",
        to=[instance.user_id.email]
    )
    msg.template_id="d-74ab4b5cbd3f4a228a87b45510361bb1"
    msg.dynamic_template_date = {
        'first_name': instance.user_id.first_name,
        'last_name': instance.user_id.last_name,
    }
    msg.send(fail_silently=False)

@shared_task
def subscription_update_paid_success(instance):
    #サブスクリプション更新支払い成功時の通知
    title="サブスクリプション更新のお支払いが完了しました"
    description="{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
        \nサブスクリプション{plan}プランへの変更が完了しました、引き続きサービスのご利用をお楽しみください。".format(first_name=instance.user_id.first_name, last_name=instance.user_id.last_name, plan=instance.plan)
    Notification.objects.create(
        user=instance.user_id,
        title=title,
        body=description
    )
    msg = EmailMessage(
        from_email="operation@enclopediai-info.com",
        to=[instance.user_id.email]
    )
    msg.template_id="d-8afc3812a6b14cbb924c3f9d25d4f35f"
    msg.dynamic_template_date = {
        'first_name': instance.user_id.first_name,
        'last_name': instance.user_id.last_name,
        'plan': instance.plan
    }
    msg.send(fail_silently=False)

from datetime import datetime, timedelta

def get_subscription_account(self):
    """deactivate plans for users whose subscriptions have been cancelled"""
    today = datetime.now(pytz.timezone('Asia/Tokyo'))
    end_day = today.replace(hour=0, minute=0, second=0)
    start_day = end_day - timedelta(days=1)
    try:
        #update_期間は削除した期間なので更新の期間ではない、start_dateから一ヶ月がサブスクリプションの終了期間となる
        accounts = StripeAccount.objects.filter(cancel_date__range=[start_day,  end_day])
        print(accounts)
        return accounts
    except:
        logger.debug('サブスクリプションを解約したユーザの削除に失敗しました 日付:{}'.format(today))
        pass

@shared_task
def subscription_delete(self):
    #サブスクリプションが削除されたときに実行される
    try:
        accounts = get_subscription_account()
        if len(accounts) > 0:
            title='サブスクリプションのご利用可能期間が終了しました'
            description='{first_name}{last_name}さまいつもEnclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
                \nサブスクリプションのご利用可能期間が終了しました,引き続きレンタルプランのご利用が可能となっております。\
                サブスクリプションをご利用を希望の方は再度申請していただく必要があります。'
            account_list = []
            for account in accounts:
                account.is_active = False
                account.update_date = None
                account.cancel_date = None
                account.plan="rental"
                account.plan_id=None
                account_list.append(account)
                Notification.objects.create(
                    user=account.user_id,
                    title=title,
                    description=description
                )

                msg = EmailMessage(
                from_email="operation@enclopediai-info.com",
                to=[account.user_id.email]
                )

                msg.template_id=""

                msg.dynamic_template_date = {
                    'frist_name': account.user_id.first_name,
                    'last_name': account.user_id.dlast_name,
                    'title': title,
                    'description': description
                }

                msg.send(fail_silently=False)
            StripeAccount.objects.bulk_update(account_list)
        else:
            logging.info('解約したユーザが存在しません')
    except:
        logging.error('サブスクリプション解約後ご利用期間終了の通知に失敗しました')
            
