from django.db import models
import uuid
from django.conf import settings
import time

def upload_img(instance, filename):
    now = time.time()
    image_filename = str(now) + str(instance.brand_name) + '.webp'
    return 'brand_icon/' + image_filename

def upload_type(instance, filename):
    now = time.time()
    image_filename = str(now) + str(instance.id) + '.webp'
    return 'type/' + image_filename
  
def upload_category(instance, filename):
    now = time.time()
    image_filename = str(now) + instance.category_name + '.webp'
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
