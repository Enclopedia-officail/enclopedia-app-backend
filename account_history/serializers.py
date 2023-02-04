from rest_framework import serializers
from product.serailizers import ProductSerializer
from .models import Favorite
from user.models import Account
from product.models import Product
import logging


logging.basicConfig(level=logging.DEBUG)

# userのお気にを全て取得
class FavoriteListSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'is_notification']
        read_only_fields = ['user', 'product']


# userを作成するために使用する
class FavoriteSerialzier(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.filter())
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter()
    )

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'is_notification']
        read_only_fields = ['user', 'product']