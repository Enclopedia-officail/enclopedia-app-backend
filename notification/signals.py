from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News, Notification, Read
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from rest_framework.response import Response
from .task import save_user_read_models
import logging

logger = logging.getLogger(__name__)

#非同期を利用してuser側での通信に遅延が起きなようにuserscreen通知とemail送信をまとめてするようにする
#非同期通信では真が可能となる
@receiver(post_save, sender=News)
def news_create_account_activitie(sender, instance, created, **kwargs):
    if created and instance.id:
        save_user_read_models(instance)

#uesrへの通知が作成された際にはactivitieカラムが作成されるようにする
@receiver(post_save, sender=Notification)
def notification_create_activitie(sender, instance, created, **kwargs):
    if created and instance.id:
        notification_type = ContentType.objects.get(app_label='notification', model='notification')
        Read.objects.create(account_id=instance.user.id, content_type=notification_type, object_id=instance.id)