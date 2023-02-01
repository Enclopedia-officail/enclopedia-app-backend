from django.db import models
from user.models import Account
from reservation.models import ReservationItem
import uuid
# Create your models here.

#クレジットカード以外の支払い
#振り込み以外の支払い方法を選択するようにする
#コンビニ決済の導入 
CREDIT = 'credit'
STORE = 'store'
method = (
    (CREDIT, 'credit'),
    (STORE, 'convenience_store_payment')
)

#reservationのなからのみ購入することができるようにする
class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='payment_account')
    payment_method = models.CharField(max_length=100, choices=method)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    amount_paid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('Accepted', 'accepted'),
        ('Completed', 'completed'),
        ('Cancelled', 'cancelled')
    )

    COUNTRY = (
        ('JP', 0.1),
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
    quantity = models.IntegerField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    

