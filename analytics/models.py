from django.db import models
from product.models import Product
from category.models import Brand

#google analyticsで取得した注目の商品を取得
class Featured(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feature_product')
    view = models.IntegerField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name

class FeaturedBrand(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='feature_brand')
    view = models.IntegerField()
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand.brand_name

class CartAddItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_add_product')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cart_add_brand')
    view = models.IntegerField()

    def __str__(self):
        return self.product.product_name