from django.contrib import admin
from . import models 
# Register your models here.

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehosue', 'prefecture', 'region')
    search_fields = ['warehouse', 'prefecture', 'region', 'address']

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('classification', 'warehouse', 'product')
    list_filter = ['classification']
    search_fields = ['product__id', 'product__product_name', 'warehouse__name']


admin.site.register(models.Warehouse, WarehouseAdmin)
admin.site.register(models.Inventory, InventoryAdmin)