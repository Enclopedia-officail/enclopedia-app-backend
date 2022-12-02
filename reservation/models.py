from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from user.models import Account
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from product.models import Product, Variation
from user.models import Account, Adress
from django.core.validators import RegexValidator

import uuid

# Create your models here.

auth_user = settings.AUTH_USER_MODEL if getattr(
    settings, "AUTH_USER_MODEL"
) else User

class Reservation(models.Model):
    REQUESTED = 0  # ユーザからリクエストが送られてきた状態
    ACCEPTED = 1  # ユーザからのリクエストを受け取った
    DENIED = 2  # ユーザからの予約リクエストを拒否した場合
    BORROWED = 3  # ユーザに商品が届き借りている状態
    SHIPPING = 4  # ユーザが商品返却ボタンで通知した場合
    RETURNED = 5  # ユーザから商品が返ってきた場合

    status = (
        (REQUESTED, _('Requested')),
        (ACCEPTED, _('Accepted')),
        (DENIED, _('Denied')),
        (BORROWED, _('Borrowed')),
        (SHIPPING, _('Shipping')),
        (RETURNED, _('Returned')),
    )

    RENTAL = 'rental'
    BASIC = 'basic'
    PREMIUM = 'premium'
    
    PLAN = (
        (RENTAL, 'rental'),
        (BASIC, 'basic'),
        (PREMIUM, 'premium'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    reserved_start_date = models.DateTimeField(auto_now_add=True)
    reserved_end_date = models.DateTimeField(blank=True, null=True)
    # 現在レンタル中かを判断するためのfield
    is_reserved = models.BooleanField(default=False)
    status = models.SmallIntegerField(choices=status, default=REQUESTED)
    plan = models.CharField(max_length=20, choices=PLAN)
    ip = models.CharField(max_length=30, blank=True)
    payment_method = models.CharField(max_length=30, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)
    shipping_price = models.IntegerField(blank=True, null=True)
    shippingNumberRegex = RegexValidator(regex= r"^\d{12}$")
    shipping_number = models.CharField(validators=[shippingNumberRegex],max_length=15, null=True, blank=True)
    return_shipping_number = models.CharField(validators=[shippingNumberRegex],max_length=15, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class ReservationItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    is_canceled = models.BooleanField(default=False)
    cancel_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.id
