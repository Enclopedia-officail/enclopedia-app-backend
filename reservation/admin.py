from django.contrib import admin
from . import models
# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'reserved_start_date', 'status', 'is_reserved')
    list_filter = ['reserved_start_date']
    search_fields = ['id']

class ReservationItemAdmin(admin.ModelAdmin):
    list_display=['id', 'product', 'quantity']
    search_fields = ['id', 'reservation__id']

admin.site.register(models.Reservation, ReservationAdmin)
admin.site.register(models.ReservationItem, ReservationItemAdmin)
