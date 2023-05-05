from django.contrib import admin
from . import models

# Register your models here.
class StylingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'age', 'height', 'weight')
    list_per_page = 100
    search_fields = ('id', 'user__id')


admin.site.register(models.Styling, StylingAdmin)
