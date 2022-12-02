from django.db import models
from django.db.models.fields import related
from product.models import Product, Variation
from user.models import Account
import uuid

class Cart(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    on_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_item', null=True)
    quantite = models.IntegerField()
    is_active = models.BooleanField(default=True)
    variation = models.ManyToManyField(Variation, blank=True, null=True)

    def total(self):
        return self.product.price.price * self.quantite

    def __unicode__(self):
        return self.product
