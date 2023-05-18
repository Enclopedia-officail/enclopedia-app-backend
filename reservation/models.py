from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from user.models import Account
from django.utils.translation import gettext_lazy as _
from product.models import Product, Variation
from user.models import Account, Adress
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from subscription.models import Payment
from django.utils import timezone
import uuid

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

    DELIVERYTIME = (
        ('指定なし', '指定なし'),
        ('午前中', '午前中'),
        ('12時〜14時頃', '12時〜14時頃'),#ゆうパックのみ
        ('14時〜16時頃', '14時〜16時頃'),
        ('16時〜18時頃', '16時〜18時頃'),
        ('18時〜20時頃', '18時〜20時頃'),
        ('19時〜21時頃', '19時〜21時頃'),
        ('20時〜21時頃', '20時〜21時頃'),

    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    reserved_day = models.DateTimeField(default=timezone.now())
    reserved_start_date = models.DateTimeField(default=timezone.now)
    reserved_end_date = models.DateTimeField(blank=True, null=True)
    # 現在レンタル中かを判断するためのfield
    is_reserved = models.BooleanField(default=False)
    status = models.SmallIntegerField(choices=status, default=REQUESTED)
    plan = models.CharField(max_length=20, choices=PLAN)
    ip = models.CharField(max_length=30, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.IntegerField(default=0, blank=True, null=True)
    shipping_price = models.IntegerField(default=0, blank=True, null=True)
    shippingNumberRegex = RegexValidator(regex= r"^\d{12}$")
    shipping_number = models.CharField(validators=[shippingNumberRegex],max_length=15, null=True, blank=True)
    return_shipping_number = models.CharField(validators=[shippingNumberRegex],max_length=15, null=True, blank=True)
    return_date = models.DateTimeField(blank=True, null=True)
    delivery_time = models.CharField(max_length=50, choices=DELIVERYTIME, default='指定なし')

    def __str__(self):
        return str(self.id)


class ReservationItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    is_canceled = models.BooleanField(default=False)
    is_bought = models.BooleanField(default=False)
    cancel_date = models.DateTimeField(blank=True, null=True)
    review = models.IntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)]
    )


    def __unicode__(self):
        return self.id
