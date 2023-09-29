from django.contrib import admin
from django.utils.safestring import mark_safe
from . import models 
import random
import string

def generate_unique_string(length=6):
    result = str(random.randint(0,999999))
    return result   

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse_name', 'prefecture', 'region')
    search_fields = ['id', 'warehouse_name', 'prefecture', 'region', 'address']

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('classification', 'warehouse', 'product')
    search_fields = ['product__id', 'product__product_name', 'warehouse__name']
    raw_id_fields = ['product']

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__id', 'user__phone_number')

class ItemAdmin(admin.ModelAdmin):
    def item_image(self, obj):
        return mark_safe('<img src="{}" style="width:100px;height:auto;">'.format(obj.img.url))
    list_display = ('number', 'item', 'price', 'bought', 'purchase', 'item_image')
    search_fields = ('number', 'purchase__id')

    def save_model(self, request, obj, form, change):
        if obj.number == '':
            num = generate_unique_string()
            obj.number = num
            obj.save()
        else:
            obj.save()

admin.site.register(models.Warehouse, WarehouseAdmin)
admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
admin.site.register(models.Item, ItemAdmin)