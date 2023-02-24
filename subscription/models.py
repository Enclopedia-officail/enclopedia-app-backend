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
    (STORE, 'convenience_store_payment')
)
#reservationのなからのみ購入することができるようにする
class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='payment_account')
    payment_method = models.CharField(max_length=100, choices=method)
    payment_id = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

