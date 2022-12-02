from rest_framework import serializers
from .models import Cart, CartItem
from product.models import Variation, Product
from .models import CartItem
from product.serailizers import VariationSerialzier, ProductSerializer

class CartSubscriptionSerializer(serializers.ModelSerializer):
    cartitems = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'on_created', 'cartitems', 'total_price']

#rentalプランようにpriceの合計を返却する必要がある、
class CartSerializer(serializers.ModelSerializer):
    cartitems = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'on_created', 'cartitems', 'total_price']

    def get_cartitems(self, obj):
        cart_items = CartItem.objects.filter(cart=obj)
        # 追加中のitemの合計数を返す
        total_quantity = 0
        for cart_item in cart_items:
            total_quantity += cart_item.quantite
        return total_quantity
    #サブスクリプション登録userでpriceがないことによるerrorが発生する
    def get_total_price(self, obj):
        total_price = 0
        try:
            cart_items = CartItem.objects.select_related('cart').filter(cart=obj)
            for cart_item in cart_items:
                total_price += cart_item.product.price.price + cart_item.quantite
            return total_price
        except:
            return  total_price


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    cart = serializers.PrimaryKeyRelatedField(
        queryset=Cart.objects.filter()
    )
    variation = serializers.PrimaryKeyRelatedField(
        queryset=Variation.objects.filter(), many=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'cart',
                  'variation', 'quantite', 'is_active']
        read_only_fields = ['product', 'variation']
