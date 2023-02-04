from django.contrib import admin
from . import models
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display =   ('id', 'user')
    list_per_page = 100
    search_fields = ['id', 'user__id']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantite', 'cart')
    list_per_page = 100
    search_fields = ['id', 'product__id', 'cart__id']

admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.CartItem, CartItemAdmin)
