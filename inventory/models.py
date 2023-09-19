from django.db import models
from product.models import Product
from user.models import Account
# Create your models here.
import time

# productが保管してある倉庫場所

def upload_img(instance, filename):
    now = time.time()
    ext = filename.split('.')[-1]
    if ext == 'webp':
            image_filename = str(now) + str(instance.id) + '.webp'
    elif ext == 'png':
        image_filename = str(now) + str(instance.id) + '.png'
    elif ext == 'jpg':
        image_filename = str(now) + str(instance.id)+'.jpg'
    return 'product/' + image_filename

#在庫保管場所
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=50)
    postalcode = models.CharField(max_length=50)
    country = models.CharField(max_length=100, default='日本')
    prefecture = models.CharField(max_length=255)
    region = models.CharField(max_length=250)
    address = models.CharField(max_length=50)
    building_name = models.CharField(
        max_length=200)

    def __str__(self):
       return self.warehouse_name

#productとは別に在庫を管理するためのtable
class Inventory(models.Model):
    STORING = 0 # 商品が入庫されていて出品していない状態　
    LEAVING = 1 # 商品が出庫されてレンタル商品として出品されている状態
    WASTE = 2 # レンタル商品として使えなくなったものの状態

    CLASSIFICATION = (
        (STORING, ('Storing')),
        (LEAVING, ('Leaving')),
        (WASTE, ('Waste'))
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name='warehouse')
    classification = models.SmallIntegerField(choices=CLASSIFICATION, default=STORING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

#買い付けた商品詳細
class Purchase(models.Model):
    #買い付け番号
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, default=None)
    created_at = models.DateField(auto_now_add=True)

#画像をこちらに保存するか考える
class Item(models.Model):
    number = models.CharField(max_length=6) #買い付けごと番号を付与する
    img = models.FileField(upload_to=upload_img, default=None, null=True)
    item = models.CharField(max_length=250)
    condition = models.CharField(max_length=250)
    price = models.IntegerField()
    bought = models.BooleanField(default=False)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)




