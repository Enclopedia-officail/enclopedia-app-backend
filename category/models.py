from django.db import models
import uuid

def upload_img(instance, filename):
    ext = filename.split('.')[-1]
    if str(ext) == 'webp':
         return 'brand_icon/' + str(instance.id) + '.' + str(ext).lower()
    else:
         return 'brand_icon/' + str(instance.id) + '.webp'


def upload_type(instance, filename):
    ext = filename.split('.')[-1]
    if str(ext) == 'webp':
         return 'type/' + str(instance.category_name) + str(instance.id) + '.' + str(ext).lower()
    else:
         return 'type/' + str(instance.category_name) + str(instance.id) + '.webp'

def upload_category(instance, filename):
    ext = filename.split('.')[-1]
    if str(ext) == 'webp':
        return 'category/' + str(instance.category_name) + str(instance.id) + '.' + str(ext).lower()
    else:
        return 'category/' + str(instance.category_name) + str(instance.id) + '.webp'


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
