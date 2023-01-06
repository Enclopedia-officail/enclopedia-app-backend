from django.contrib import admin
from product.models import Product, Size, Shipping, Price, Variation, ReviewRating, ImageGallary, Tag

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'stock', 'gender')
    list_filter = ['created_at']
    list_per_page = 100
    search_fields = ['id', 'product_name']

class ImageGallaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')
    list_per_page = 100
    search_fields = ['product__id', 'product__product_name']
    raw_id_fields = ['product']

class VariationAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'variation_choices', 'variation_value')
    search_fields = ['product__id', 'product__product_name']

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating')
    list_per_page = 100
    search_fields = ['user__id', 'user__email', 'product__id', 'product__product_name']

class PriceAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ('id', 'price', 'shipping')

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id', 'shipping_company', 'shipping_method', 'size', 'shipping_price')

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag_name')
    list_per_page = 100

class SizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size')
    list_per_page = 100
    search_fields = ['product__id', 'product__product_name']

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ImageGallary, ImageGallaryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Shipping, ShippingAdmin)
admin.site.register(Price, PriceAdmin)
