from rest_framework import serializers
from .models import Payment, Order, OrderItem
from user.serializers import AccountSerializer
from reservation.serializers import ReservationItemSerializer

class PaymentSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_method', 'payment_id', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'order_id', 'total_price', 'created_at']

#orderitemが確定しユーザが商品を購入した場合には返却されなくて済むうにする
class OrderItemSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    order = OrderSerializer(read_only=True)
    reservation_item = ReservationItemSerializer

    class Meta:
        model = OrderItem
        fields = ['id', 'payment', 'order', 'reservation_item', 'created_at', 'updated_at']