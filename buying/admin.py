from django.contrib import admin
from . import models
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_method', 'payment_id', 'created_at')
    list_per_page = 100
    search_fields = ['id', 'user__id', 'payment_id']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment', 'order_id', 'total_price', 'tax', 'status', 'ip', 'created_at', 'updated_at')
    list_per_page = 100
    search_fields = ['id', 'user__id', 'order_d']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'reservation_item', 'is_ordered', 'created_at', 'updated_at')
    list_per_page = 100
    search_fields = ['id', 'reservation_item__id', 'reservation_item__product__id']

admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)