from django.contrib import admin
from .models import Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_per_page = 100
    search_fields = ('id', 'user__id', 'product__id')

# Register your models here.
admin.site.register(Favorite, FavoriteAdmin)
