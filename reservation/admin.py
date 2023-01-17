from django.contrib import admin
from . import models
import datetime
# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display=('id', 'user', 'reserved_start_date', 'status', 'is_reserved')
    list_filter = ['reserved_start_date']
    search_fields = ['id']
    
    def save_model(self, request, obj, form, change):
        update_fields = []
        if change:
            if form.cleaned_data ==3:
                update_fields.append('status')
                update_fields.append('shipping_number')
                obj.save(update_fields=update_fields)
            elif form.cleaned_data == 5:
                update_fields.append('status')
                update_fields.append('return_date')
                time = datetime.datetime.now()
                obj.return_date = time
                obj.save(update_fields=update_fields)
            else:
                obj.save()
        else:
            obj.save()



class ReservationItemAdmin(admin.ModelAdmin):
    list_display=['id', 'product', 'quantity']
    search_fields = ['id', 'reservation__id']
    raw_id_fields = ['product']


    def save_model(self, request, obj, form, change):
        update_fields = []
        if change:
            if form.initial['review'] != form.cleaned_data['review']:
                update_fields.append('review')
        obj.save(update_fields=update_fields)

admin.site.register(models.Reservation, ReservationAdmin)
admin.site.register(models.ReservationItem, ReservationItemAdmin)
