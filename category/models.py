from django.db import models
import uuid
from PIL import Image
from django.conf import settings
import os
import boto3

def upload_img(instance, filename):
    ext = filename.split('.')[-1]
    if str(ext) == 'webp':
        return 'brand_icon/' + str(instance.brand_name) + '.' + str(ext).lower()
    else:
        image = Image.open(instance.img)
        image_filename = str(instance.brand_name) + '.webp'
        path = os.path.join('media/brand_icon/', image_filename)
        local_path = os.path.join('media' + image_filename)
        image.save(local_path, format='webp')
        s3 = boto3.client('s3')
        s3.upload_file(local_path, "enclopedia-media-bucket", path)
        os.remove(local_path)
        return 'brand_icon/' + image_filename


def upload_type(instance, filename):
    ext = filename.split('.')[-1]
    image_filename = str(instance.id) + '.webp'
    if str(ext) == 'webp':
        return 'type/' + image_filename
    else:
        image = Image.open(instance.image)
        path = os.path.join('media/type', image_filename)
        local_path = os.path.join('media', image_filename)
        image.save(local_path, format='webp')
        s3 = boto3.client('s3')
        s3.upload_file(local_path, "enclopedia-media-bucket", path)
        os.remove(local_path)
        return 'type/' + image_filename 

def upload_category(instance, filename):
    ext = filename.split('.')[-1]
    if str(ext) == 'webp':
        return 'category/' + str(instance.category_name) + str(instance.id) + '.' + str(ext).lower()
    else:
        image = Image.open(instance.image)
        image_filename = instance.category_name + '.webp'
        path = os.path.join('media/category/', image_filename)
        local_path = os.path.join('media/', image_filename)
        image.save(local_path, format='webp')
        s3 = boto3.client('s3')
        s3.upload_file(local_path, "enclopedia-media-bucket", path)
        os.remove(local_path)
        return 'category/' + image_filename


class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    category_name = models.CharField(max_length=30, unique=True)
    image = models.FileField(upload_to=upload_type)

    class Meta():
        verbose_name = 'タイプ'
        verbose_name_plural = 'タイプ'

    def __str__(self):
        return self.category_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    image = models.FileField(upload_to=upload_category)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True, related_name='type')

    class Meta():
        verbose_name = 'カテゴリー'
        verbose_name_plural = 'カテゴリー'

    def __str__(self):
        return str(self.category_name)

class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)
    img = models.FileField(upload_to=upload_img, blank=True, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    class Meta():
        verbose_name = 'ブランド'
        verbose_name_plural = 'ブランド'

    def __str__(self):
        return str(self.brand_name)
