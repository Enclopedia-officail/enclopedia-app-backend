from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from user.models import Account, Adress, Profile, EmailSubscribe, AuthPhoneNumber, Credibility
from subscription.models import StripeAccount
from django_rest_passwordreset.signals import reset_password_token_created
from .tasks import create_sendgrid_contact, send_register_confirmation_email, send_confirmation_email, password_reset
from .tasks import send_social_login_register_email, authentication_phone_number

#from axes.signals import user_locked_out
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Account)
def create_account_profile(sender, instance, created, **kwargs):
    if created and instance.id:
        Profile.objects.create(user=instance)
        Adress.objects.create(user=instance)
        Credibility.objects.create(user=instance)
        StripeAccount.objects.create(user_id=instance)

#accout作成時にsendgrid mailingリストにメールを登録し、EmailSubscribetableを作成する
@receiver(post_save, sender=Account)
def add_sendgrid_maling_list(sender, instance, created, **kwargs):
    try:
        if created and instance.id:
            EmailSubscribe.objects.create(user=instance)
            create_sendgrid_contact(instance)
    except:
        logger.error('sendgridユーザ登録 user:{} sendgridユーザ登録に失敗しました。')

#アカウント作成時に仮登録完了のメールを送信するようにする
@receiver(post_save, sender=Account)
def send_register_confirmation(sender, instance, created, **kwargs):
    if instance.is_active == False:
        if created and instance.id:
            send_register_confirmation_email(instance)
        else:
            pass
    else:
        if created:
            send_social_login_register_email(instance)
        else:
            pass
        
#password resetする際のメールsendgridで送信する
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    password_reset(instance, reset_password_token)
    
#本登録完了の際にmailを送信する
@receiver(pre_save, sender=Account)
def confirmation_send_mail(sender, instance, update_fields, *args, **kwargs):
    if update_fields is None:
        pass
    else:
        if ("is_active" in list(update_fields)) & (instance.is_active == True):
            send_confirmation_email(instance)
        else:
            logger.error('本登録完了通知 user:{} メール送信に失敗しました。')
            pass
@receiver(post_save, sender=AuthPhoneNumber)
def delete_auth_phonenumber(sender, instance, created, **kwargs):
    if created and instance:
        authentication_phone_number(instance)
    else:
        logger.error('電話番号削除用認証番号の削除に失敗しました') 
