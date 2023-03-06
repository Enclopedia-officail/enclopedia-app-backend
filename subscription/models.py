from django.db import models
from django.conf import settings
from user.models import Account
import uuid

class StripeAccount(models.Model):
    """user that registered subscripiton"""
    RENTAL = 'rental'
    BASIC = 'basic'
    PREMIUM = 'premium'
    PLAN = (
        (RENTAL, 'rental'),
        (BASIC, 'basic'),
        (PREMIUM, 'premium'),
    )
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE
    )
    customer_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    plan = models.CharField(max_length=20, choices=PLAN,
                            blank=True, null=True, default='rental')
    plan_id = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    cancel_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.customer_id)

CREDIT = 'card'
STORE = 'store'
method = (
    (CREDIT, 'card'),
    (STORE, 'store')
)
#reservationのなからのみ購入することができるようにする
class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='payment_account')
    payment_method = models.CharField(max_length=100, choices=method)
    payment_id = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
currency = (
    ('jpy', 'jpy'),
)

duration = (
    ('once', 'once'),
    ('repeting', 'repeting'),
    ('forever', 'forever')
)

class Coupon(models.Model):
    #独自のidを発行
    #値引き料
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    amount_off = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    #使用通過
    currency = models.CharField(max_length=3, choices=currency, default='jpy')
    #クーポン使用回数
    duration = models.CharField(max_length=30, choices=duration)
    #サブスクリプションで下記で指定された分割引く
    duration_month = models.IntegerField()
    #クーポンの発行枚数
    max_redemptions = models.IntegerField()
    name = models.CharField(max_length=50)
    percent_off = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    times_redeemed = models.IntegerField()
    redeem_by = models.DateField()

    def __str__(self):
        return self.name


