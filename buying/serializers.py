from rest_framework import serializers
from .models import Payment, Order, OrderItem
from user.serializers import AccountSerializer
from reservation.serializers import ReservationItemSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_method', 'payment_id', 'amount_paid', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user',  'payment', 'order_id', 'total_price', 'tax', 'status', 'created_at']

#orderitemが確定しユーザが商品を購入した場合には返却されなくて済むうにする
class OrderItemSerializer(serializers.ModelSerializer):

    order = OrderSerializer(read_only=True)
    user = AccountSerializer(read_only=True)
    reservation_item = ReservationItemSerializer

    class Meta:
        model = OrderItem
        fields = ['id','user', 'order', 'reservation_item', 'is_ordered', 'created_at', 'updated_at']