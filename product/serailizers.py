from rest_framework import serializers
from .models import Product, Shipping, Size, Price, Tag, Variation, ReviewRating, ImageGallary, ReviewRatingGallery
from user.serializers import AccountSerializer, ReviewUserSerializer
from category.serializers import BrandSerializer
from account_history.models import Favorite
from user.models import Account


import logging

logging.basicConfig(level=logging.DEBUG)


class SizeSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter()
    )

    class Meta:
        model = Size
        fields = ['id', 'product', 'size', 'length', 'shoulder_width', 'chest',
                  'waist', 'hip', 'rise', 'inseam', 'hem_width', 'sleeve_length']
        lookup_filed = 'product'


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['shipping_company',
                  'shipping_method', 'size', 'shipping_price']


class PriceSerializer(serializers.ModelSerializer):
    shipping = ShippingSerializer(read_only=True)

    class Meta:
        model = Price
        fields = ['id', 'shipping', 'price', 'tax']


# タグからproductlistを取得するためのview


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'tag_name']

# productの詳細のみを取得するときには全ての情報を取得するようにする


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    price = PriceSerializer(read_only=True)
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description',
                  'rating', 'review_count', 'stock', 'img', 'is_available',  'is_subscription',
                  'brand', 'tag', 'price', 'gender', 'buying_price']

class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    price = PriceSerializer(read_only=True)
    tag = TagSerializer(read_only=True, many=True)
    number_of_like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description',
                  'rating', 'review_count', 'stock', 'img', 'is_available',  'is_subscription',
                  'brand', 'tag', 'size', 'price', 'buying_price', 'gender', 'number_of_like',  'buying_price']
    
    def get_number_of_like(self, obj):
        favorites = Favorite.objects.filter(product=obj)
        return len(favorites)

# productLIstの時はidとimage,prduct/nameを取得s流用んしる


class ProductCategoryListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'img',
                  'is_available','brand', 'category', 'gender', 'stock', 'is_subscription']


# 性別ごとにproductsを取得


class ProductGenderSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    size = SizeSerializer(many=True, read_only=True)
    price = PriceSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'slug', 'description',
                  'rating', 'stock', 'img', 'is_available',  'is_subscription',
                  'brand', 'size', 'price', 'gender']
        lookup_field = 'gender'


class VariationSerialzier(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    variation_choices = serializers.ChoiceField(
        choices=['color', 'size', 'condition']
    )

    class Meta:
        model = Variation
        fields = ['id', 'product', 'variation_choices',
                  'variation_value', 'is_active', 'created_on']
        lookup_field = 'product'


# reviewを取得する際はproductidを識別としてlistで取得


class ReviewListSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter()
    )
    user = ReviewUserSerializer(read_only=True)
    on_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ReviewRating
        fields = ['id', 'user', 'product', 'title', 'review',
                  'rating', 'status', 'on_created']
        lookup_field = 'product'


# user個々人の投稿を制御するためのシリアライザー


class UserReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    user = AccountSerializer(read_only=True)
    on_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ReviewRating
        fields = ['product', 'user', 'title', 'review', 'rating', 'ip',
                  'status', 'on_created']


# reviewのimageギャラリーを変更するときはトランザクションで処理する必要がある。


class ReviewRatingSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.filter()
    )
    on_created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ReviewRating
        fields = ['id', 'product', 'user', 'title', 'review', 'rating',
                  'status', 'on_created']

        lookup_field = 'product'
        read_only_fields = ('user', 'product')

# reviewの画像ギャラリーのためのseriazlier


class ImageGallarySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter()
    )

    class Meta:
        model = ImageGallary
        fields = ['id', 'product', 'original']
        lookup_field = 'product'
