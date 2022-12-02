from django.contrib import admin
from product.models import Product, Size, Shipping, Price, Variation, ReviewRating, ImageGallary, Tag

admin.site.register(Product)
admin.site.register(Variation)
admin.site.register(ReviewRating)
admin.site.register(ImageGallary)
admin.site.register(Size)
admin.site.register(Tag)
admin.site.register(Shipping)
admin.site.register(Price)
