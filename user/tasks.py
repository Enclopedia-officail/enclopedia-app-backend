from django.conf import settings
from celery import shared_task
from django.core.mail import EmailMessage
from notification.models import Notification
import environ
import json
import requests

import logging
logger = logging.getLogger(__name__)

env = environ.Env()

@shared_task
def create_sendgrid_suppressions(instance):
    try:
        secret = settings.SENDING_API_KEY
        header = {'Content-type':'application/json', 'Authorization':'Bearer ' + secret}
        url = 'https://api.sendgrid.com/v3/asm/groups/{}/suppressions'.format('30160')
        data = {
                "recipient_emails":[
                    instance.email
                ]
            }
        requests.post(url, headers=header, data=json.dumps(data))
    except:
        logger.error('sendgrid email送信リスト登録 user:{} 登録失敗'.format(instance.id))
        pass

#今回はuserのidをurlに付与してfrontendに渡すがここをtokenに置き換えを行う。
@shared_task
def send_register_confirmation_email(instance):
    msg = EmailMessage(
        from_email='operation@enclopediai-info.com',
        to=[instance.email]
    )
    msg.template_id="d-5eef9d80ad9b4d468e8e02cb6eabff9e"
    msg.dynamic_template_data = {
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'Weblink': '{domain}/{url}/{id}'.format(domain=env("FRONTEND_URL"), url="register_confirmed", id=instance.id)
    }
    msg.send(fail_silently=False)

#social login
@shared_task
def send_social_login_register_email(instance):
    title="アカウント登録が完了しました"
    body='{first_name}{last_name}様Enclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
        \nアカウント登録が完了致しました、早速Enclopediaが提供するアイテムをレンタルすることができます。'.format(first_name=instance.first_name, last_name=instance.last_name)
    Notification.objects.create(
        user=instance,
        title=title,
        body=body
    )
    msg = EmailMessage(
        from_email='operation@enclopediai-info.com',
        to=[instance.email]
    )
    msg.template_id="d-40e6a9b016c6484ca7c24d6dc44a4cfb"
    msg.dynamic_template_data = {
        'first_name': instance.first_name,
        'last_name': instance.last_name
    }
    msg.send(fail_silently=False)


#本登録完了後に送信する
@shared_task
def send_confirmation_email(instance):
    try:
        title="アカウント登録が完了しました"
        body='{first_name}{last_name}様Enclopediaファッションレンタルサービスをご利用いただきありがとうございます。\
            \nアカウント登録が完了致しました、早速Enclopediaが提供するアイテムをレンタルすることができます。'.format(first_name=instance.first_name, last_name=instance.last_name)
        Notification.objects.create(
            user=instance,
            title=title,
            body=body
        )    
        msg = EmailMessage(
            from_email='operation@enclopediai-info.com',
            to=[instance.email]
        )
        msg.template_id='d-135b5de149c748e0a70f1bda12cc7bed'
        msg.dynamic_template_data = {
            'first_name':instance.first_name,
            'last_name':instance.last_name,
            'Weblink':'{domain}/login'.format(domain=env("FRONTEND_URL"))
        }
        msg.send(fail_silently=False)
    except:
        logging.info('本登録完了通知Email user:{} 送信失敗'.format(instance.id))
        pass

#passwordを変更をするためのmailを送信する
@shared_task
def password_reset(instance, reset_password_token):
    msg = EmailMessage(
        from_email="operation@enclopediai-info.com",
        to=[reset_password_token.user.email]
    )
    msg.template_id='d-ecea36058619453eb203e17768fa7128'
    msg.dynamic_template_data = {
        "first_name":reset_password_token.user.first_name,
        "last_name":reset_password_token.user.last_name,
        "Weblink":'{domain}/{url}?token={token}'.format(domain=env("FRONTEND_URL"),url='/password_reset/password/confirm', token=reset_password_token.key)
    }
    msg.send(fail_silently=False)

#電話番号認証用番号を送信
@shared_task
def authentication_phone_number(instance):

    msg = EmailMessage(
        from_email="operation@enclopediai-info.com",
        to=[instance.user.email]
    )
    print('send')
    msg.template_id = "d-bcb56a6c49414a70b98fc573042dbdef"
    msg.dynamic_template_data = {
        "authentication_number": instance.random_number.number
    }
    print('finish')
    msg.send(fail_silently=False)
