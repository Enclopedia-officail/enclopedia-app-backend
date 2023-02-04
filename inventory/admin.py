from django.contrib import admin
from . import models 
# Register your models here.

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse_name', 'prefecture', 'region')
    search_fields = ['id', 'warehouse_name', 'prefecture', 'region', 'address']

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('classification', 'warehouse', 'product')
    search_fields = ['product__id', 'product__product_name', 'warehouse__name']
    raw_id_fields = ['product']


admin.site.register(models.Warehouse, WarehouseAdmin)
admin.site.register(models.Inventory, InventoryAdmin)