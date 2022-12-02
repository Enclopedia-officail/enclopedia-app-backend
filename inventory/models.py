from django.db import models
from product.models import Product
# Create your models here.

# productが保管してある倉庫場所

#在庫保管場所
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=50)
    postalcode = models.CharField(max_length=50)
    prefecture = models.CharField(max_length=255, default=None, null=True)
    region = models.CharField(max_length=250, default=None, null=True)
    address = models.CharField(max_length=50, default=None, null=True)
    building_name = models.CharField(
        max_length=200, default=None, blank=True, null=True)

#productとは別に在庫を管理するためのtable


class Inventory(models.Model):
    STORING = 0 # 商品が入庫されている状態
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


