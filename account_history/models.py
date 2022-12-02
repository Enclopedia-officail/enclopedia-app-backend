from django.db import models
from user.models import Account
from product.models import Product
# Create your models here.
# 保存できる数をあらかじめ決定しておいてその数に達した場合に自動的に古い履歴は削除されるようにする
# 検索履歴、購入履歴、履歴を使用したおすすめすすめなど

# このアプリケーションはuserと統合する方が良い

# cronを利用して１日の終わりにdbに登録する

class Favorite(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='favorite_product')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def count(self):
        count = Favorite.objects.filter(product=Product('id')).count()
        return count