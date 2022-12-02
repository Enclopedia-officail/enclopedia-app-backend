from rest_framework import serializers
from .models import Closet, Cloth
from product.serailizers import ProductSerializer
from product.models import Product
import logging


logging.basicConfig(level=logging.DEBUG)

# userでlist取得するためのserializer


class ClosetCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Closet
        fields = ['id', 'closet_name', 'description']


class ClosetSerializer(serializers.ModelSerializer):
    closet = serializers.StringRelatedField(many=True)
    cloth = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Closet
        fields = ['id', 'closet_name', 'description',
                  'created_at', 'updated_at', 'closet', 'cloth']
        lookup_fields = ['user']
    def get_cloth(self, obj):
        clothes = Cloth.objects.filter(closet=obj)
        serializer = ClothSerializer(clothes, many=True)
        return serializer.data

class ClothSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Cloth
        fields = ['id', 'product', 'created_at']

class ClothCreateSerializer(serializers.ModelSerializer):
    closet = serializers.PrimaryKeyRelatedField(
        queryset=Closet.objects.filter()
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter()
    )

    class Meta:
        model = Closet
        fields = ['id', 'product', 'closet']
