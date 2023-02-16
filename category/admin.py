from django.contrib import admin
from .models import Category, Brand, Type

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'type', 'created_at')
    search_fields = ['id', 'category_name', 'type__id', 'type_category_name']

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand_name')
    list_per_page = 100
    search_fields = ['id', 'brand_name']

class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at')
    search_fields = ('id', 'category_name')
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Type, TypeAdmin)
