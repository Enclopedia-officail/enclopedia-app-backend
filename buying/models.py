from django.db import models
from user.models import Account
from reservation.models import ReservationItem
from subscription.models import Payment
import uuid
# Create your models here.

#クレジットカード以外の支払い
#振り込み以外の支払い方法を選択するようにする
#コンビニ決済の導入 

class Order(models.Model):
    STATUS = (
        ('Accepted', 'accepted'),
        ('Completed', 'completed'),
        ('Denied', 'denied'),
        ('Cancelled', 'cancelled')
    )

    COUNTRY = (
        ( 0.1, 'JP'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='order_account', null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, related_name='order_payment', null=True)
    order_id = models.CharField(max_length=100, unique=True)
    total_price = models.IntegerField()
    tax = models.FloatField(choices=COUNTRY)
    status = models.CharField(max_length=100, choices=STATUS)
    ip = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True,  related_name='order_item_account')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    reservation_item = models.ForeignKey(ReservationItem, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)