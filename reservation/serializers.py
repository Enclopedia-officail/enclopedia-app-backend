from django.db.models.query_utils import Q
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import Reservation, ReservationItem
from user.models import Account, Adress
from product.models import Product, Variation
from product.serailizers import ProductSerializer, VariationSerialzier
from subscription.models import StripeAccount


class ReservationSerializr(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=[0, 1, 2, 3, 4, 5]
    )

    class Meta:
        model = Reservation
        fields = ['id', 'reserved_start_date', 'reserved_end_date', 'is_reserved',
                  'status', 'plan', 'total_price', 'shipping_price', 'shipping_number', 'return_shipping_number']

#shipping情報とstatusを入れ替える
class ReservationShippingNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'status', 'shipping_number']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.shipping_number = validated_data.get('shipping_number', instance.shipping_number)
        instance.save(update_fields=["status"])
        return instance

#返却時のreturn_shipping_numberとstatusのupdate
class ReservationReturnShippingNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'status', 'return_shipping_number']
        
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.return_shipping_number= validated_data.get('return_shipping_number', instance.return_shipping_number)
        instance.save(update_fields=["status", 'return_shipping_number'])
        return instance
    
class ResrevationListSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=[0, 1, 2, 3, 4, 5]
    )

    reservation_items = SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['id', 'reserved_start_date', 'reserved_end_date', 'is_reserved',
                  'status', 'plan', 'total_price', 'shipping_price', 'shipping_number', 'reservation_items']

    def get_reservation_items(self, obj):
        try:
            reservation_items = ReservationItem.objects.select_related('product', 'reservation').filter(reservation__id=obj.id)
            serializer = ReservationItemSerializer(reservation_items, many=True)
            return serializer.data
        except:
            reservation_items = []
            return reservation_items



class ReservationItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    reservation = ReservationSerializr(read_only=True)

    class Meta:
        model = ReservationItem
        fields = ['id', 'product', 'reservation', 'quantity']

#product内の
class ReservationItemUserSerializer(serializers.ModelSerializer):
    reservation_item = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Reservation
        fields = ['id', 'reservation_item']
    def get_reservation_item(self, obj):
        reservation_items = ReservationItem.objects.select_related('product', 'reservation').filter(reservation__id=obj.id)
        serializer = ReservationItemSerializer(reservation_items, many=True)
        return serializer.data
    
    
