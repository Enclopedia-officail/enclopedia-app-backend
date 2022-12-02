from django.db import models
from user.models import Account
from product.models import Product
from django.utils.translation import gettext_lazy as _

class Closet(models.Model):

    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='user_closet')
    closet_name = models.CharField(max_length=100,blank=False, null=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.closet_name

class Cloth(models.Model):
    closet = models.ForeignKey(
        Closet, on_delete=models.CASCADE, related_name='closet')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='closet_product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '/media/{}'.format(self.product.img)
