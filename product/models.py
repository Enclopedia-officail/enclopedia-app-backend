from category.models import Category, Brand
from django.db import models
from django.db.models import Avg, Count
from django.core.validators import MinValueValidator, MaxValueValidator
from user.models import Account
from PIL import Image
import boto3
import os
import datetime
import uuid

def upload_img(instance, filename):
    today = datetime.datetime.now()
    ext = filename.split('.')[-1]

    if str(ext) == 'webp':
        #s3に保存
        return 'image_gallary/' + str(today) + str(instance.id) + '.' + str(ext).lower()
    else:
        image = Image.open(instance.img)
        image_filename = str(today) + str(instance.id) + '.webp'
        path = os.path.join("media/image_gallary", image_filename)
        image.save(image_filename, "WEBP")
        #s3に保存
        s3 = boto3.client('s3')
        s3.upload_file(path, "enclopedia-media-bucket", path)
        os.remove(path)
        return path

def upload_review_img(instance, filename):

    ext = filename.split('.')[-1]
    if str(ext) == 'webp':
        return 'review/' + str(instance.id) + '.' + str(ext).lower()
    else:
        return 'review/' + str(instance.id) + '.webp'
    
def upload_thumbnail(instance, filename):

    ext = filename.split('.')[-1]
    if str(ext) == 'webp':
        return 'image_gallary/thumbnail/' + str(instance.product.id + instance.id) + '.' + str(ext).lower()
    else:
        return 'image_gallary/thumbnail/' + str(instance.product.id + instance.id) + '.webp'

def upload_product(instance, filename):
    ext = filename.split('.')[-1]
    image = Image.open(instance.img)
    #webpをs3に保存することでWebサイトの改善を図る  
    if str(ext) == 'webp':
        return 'product/' + str(instance.id) + '.' + str(ext).lower()
    else:
        path = os.path.join('media/product/'+str(instance.id)+'.webp')
        image.save(path, 'WEBP')
        s3 = boto3.client('s3')
        s3.upload_file(path, "enclopedia-media-bucket", path)
        os.remove(path)
        return path

# 配送料を決定するための
shipping_size = [
    ('ネコポス', 'ネコポス'),
    ('宅急便コンパクト', '宅急便コンパクト'),
    ('0', '0'),
    ('60', '60'),
    ('80', '80'),
    ('100', '100'),
    ('120', '120'),
    ('140', '140'),
    ('160', '160'),
]

class Shipping(models.Model):
    shipping_company = models.CharField(max_length=30)
    shipping_method = models.CharField(max_length=30)
    size = models.CharField(max_length=100, blank=True, choices=shipping_size)
    shipping_price = models.IntegerField()

    def __str__(self):
        return self.shipping_method

taxes = [
    (0.1, 0.1)
]

class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shipping = models.ForeignKey(
        Shipping, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField()
    tax = models.FloatField(choices=taxes, blank=True, null=True)

    def __str__(self):
        return str(self.price) + 'サイズ:' + str(self.shipping.size)

    def total_price(self):
        return (self.prince + self.shipping.price)*self.tax


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_name

plan_choices = [
    ('rental', 'rental'),
    ('basic', 'basic'),
    ('premium', 'premium'),
]

gender_choice = [
    ('メンズ', 'mens'),
    ('レディース', 'ladies'),
    ('キッズ', 'kids')
]


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, unique=True)
    product_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, blank=True, null=True, default=0.0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(5.0)]
    )
    review_count = models.IntegerField(blank=True, null=True, default=0)
    stock = models.IntegerField(default=0)
    img = models.FileField(upload_to=upload_product,
                           default=None, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_subscription = models.CharField(max_length=100, choices=plan_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, related_name='products', null=True, blank=True
    )
    tag = models.ManyToManyField(
        Tag, related_name='product_tag', null=True, blank=True)
    price = models.ForeignKey(
        Price, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    buying_price = models.IntegerField(default=0)
    gender = models.CharField(
        max_length=10, choices=gender_choice, default="mens")

    def __str__(self):
        return self.product_name

    # レビューの平均値を取得する
    def rating_average(self):
        ratings = ReviewRating.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if ratings['average'] is not None:
            avg = float(ratings['average'])
            return avg
        return ratings

    # レビュー数を取得する
    def count_review(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def count_favorite(self):
        favorites = Favorite.objects.filter(
            product=self).aggregate(count=Count('id'))
        if favorites['count'] is not None:
            count = int(favorites['count'])
        return count

cloth_size = (
    ('XS', 'xs'),
    ('S', 's'),
    ('M', 'm'),
    ('L', 'l'),
    ('XL', 'xl'),
    ('XXL', 'xxl'),
    ('FREE', 'free')
)

class Size(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='size')
    size = models.CharField(max_length=10, choices=cloth_size)
    length = models.IntegerField(blank=True, null=True)
    shoulder_width = models.IntegerField(blank=True, null=True)
    chest = models.IntegerField(blank=True, null=True)
    waist = models.IntegerField(blank=True, null=True)
    hip = models.IntegerField(blank=True, null=True)
    rise = models.IntegerField(blank=True, null=True)
    inseam = models.IntegerField(blank=True, null=True)
    hem_width = models.IntegerField(blank=True, null=True)
    sleeve_length = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.size


category_choices = (
    ('カラー', 'Color'),
    ('コンディション', 'condition'),
)

"""商品のコンディション"""
condition_choices = [
    ( '新品', 'unused' ),
    ( '未使用に近い','near_unused' ),
    ( '目立った汚れなし', 'no_stain' ),
    ( 'やや汚れあり', 'slightly_stain' ),
    ( '汚れあり', 'stain' )
]

# variationで各サイズの
#各バリエーションのstock数をどのように把握するのかが必要

class Variation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_variation')
    variation_choices = models.CharField(
        max_length=100, choices=category_choices
    )
    variation_value = models.CharField(max_length=100, choices=condition_choices)
    is_active = models.BooleanField(default=True)
    #stack = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.product

class ReviewRating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_review')
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='user_review')
    title = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(blank=True, null=True)
    ip = models.CharField(max_length=30, blank=True)
    status = models.BooleanField(default=True)
    on_created = models.DateTimeField(auto_now_add=True)
    on_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ReviewRatingGallery(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    review = models.ForeignKey(
        ReviewRating, on_delete=models.CASCADE, related_name='review_gallery')
    image = models.FileField(upload_to=upload_review_img)
    on_created = models.DateTimeField(auto_now_add=True)
    on_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.review.title)

class ImageGallary(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_image')
    original = models.FileField(upload_to=upload_img)
    # からは推奨されないのでseiralizerで制御する

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'image gallary'
        verbose_name_plural = 'image gallary'
