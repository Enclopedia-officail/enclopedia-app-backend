from django.db import models
from django.conf import settings

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
