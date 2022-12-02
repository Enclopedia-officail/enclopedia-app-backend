from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from .models import Read
from user.models import Account

#emailds
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

import environ
import logging
logger = logging.getLogger(__name__)

env = environ.Env()

##newsが作成されrば非同期とシグナルでカラムを一気に作成させるようにする
@shared_task
def save_user_read_models(instance):
    reads = []
    users = Account.objects.all()
    news_type = ContentType.objects.get(app_label='notification', model='news')
    for user in users:

        read = Read(account_id=user.id,content_type=news_type , object_id=instance.id)
        reads.append(read)
    #bulk_createを使用することで処理を速くする
    Read.objects.bulk_create(reads)

@shared_task
#mail通知に対して有無はuserが無効化有効にできるようにする
#userに対して通知を行なった際に
def save_user_read_send_email(instance):
    users = Account.objects.all()
    #全てのuserに通知を送るようにする
    for user in users:
        context = {
            'domain': env("BACKEND_URL"),
            'username': user.username,
            'email': user.email,
            'register_confirmation_url': '{url}/{id}'.format(url='api/account/register_confirm', id=instance.id)
        }

        email_plain_text = render_to_string(
            'account_form/account_register_confirmation.html', context
        )

        send_mail(
            'Enclopedia運営',
            email_plain_text,
            settings.EMAIL_HOST_USER,
            [user.email]
        )




