from django.db import models
from user.models import Account
from product.models import Product

class Favorite(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='favorite_product')
    created_at = models.DateTimeField(auto_now_add=True)
    is_notification = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def count(self):
        count = Favorite.objects.filter(product=Product('id')).count()
        return count