from django.contrib import admin
from .models import StripeAccount

class StripeAccountAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'user_id', 'plan', 'is_active')
    search_fields = ['customer_id', 'user_id__email']

# Register your models here.
admin.site.register(StripeAccount, StripeAccountAdmin)
