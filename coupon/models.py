from django.db import models
from user.models import Account
from django.core.validators import RegexValidator
import uuid

currency = (
    ('jpy', 'jpy'),
)

duration = (
    ('once', 'once'),
    ('repeting', 'repeting'),
    ('forever', 'forever')
)

type = (
    ('subscription', 'subscription'),
    ('rental', 'rental'),
    ('purchase', 'purchase')
)

class Coupon(models.Model):
    #独自のidを発行
    #値引き料
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    type = models.CharField(max_length=30, choices=type)
    #顧客の少額から差し引かられる料金
    amount_off = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    #使用通貨
    currency = models.CharField(max_length=3, choices=currency, default='jpy')
    #クーポン使用回数
    duration = models.CharField(max_length=30, choices=duration)
    #継続期間が繰り返しの場合、クーポンが適用される月数
    duration_in_month = models.IntegerField(null=True, default=None)
    #継続期間が繰り返しの場合、クーポンが適用される回数
    duration_in_times = models.IntegerField(default=1)
    #クーポンを最大発   行できる枚数
    max_redemptions = models.IntegerField()
    name = models.CharField(max_length=50)
    #パーセンテージで割り引く
    percent_off = models.DecimalField(max_digits=3, decimal_places=2, null=True, default=None)
    #このクーポンが顧客に発行された枚数
    times_redeemed = models.IntegerField(default=0)
    #クーポンが利用できなくなる日
    redeem_by = models.DateField()
    #クーポンを顧客に適用できるか
    valid = models.BooleanField(default=True)

    def __str__(self):
        return self.name

#couponの発行と使用の管理
class Issuing(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    duration = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)
    expiration = models.DateField(null=True, default=None)

#userが作成されると同時にこちらの作成もされる必要がある
class InvitationCode(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)

class Invitation(models.Model):
    InvitationCode = models.ForeignKey(InvitationCode, on_delete=models.SET_NULL, null=True)
    phoneNumberRegex = RegexValidator(regex = r"^\d{8,16}$")
    phone_number =models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True, blank=True, null=True)
