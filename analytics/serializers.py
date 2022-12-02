from rest_framework import serializers
from .models import Featured,FeaturedBrand, CartAddItem
from product.serailizers import ProductSerializer
from category.serializers import BrandSerializer
#google analyticsで割り出した統計を利用して人気の商品の定義を行うようにする

class FaturedSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = Featured
        fields = ['id', 'product', 'url', 'view']

class FeatureBrandSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = FeaturedBrand
        fields = ['id', 'brand', 'url']

class CartAddItemSerializesr(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = CartAddItem
        fields = ['id', 'product', 'brand', 'view']
