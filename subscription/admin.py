from django.contrib import admin
from .models import StripeAccount, Payment, Coupon

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_method', 'payment_id', 'created_at')
    list_per_page = 100
    search_fields = ['id', 'user__id', 'payment_id']


class StripeAccountAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'user_id', 'plan', 'is_active')
    search_fields = ['customer_id', 'user_id__email']

class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'amount_off', 'created_at', 'currency', 'duration', 'duration_in_month', 'max_redemptions', 'name', 'percent_off', 'times_redeemed', 'redeem_by')
    search_fields = ['id',]

# Register your models here.
admin.site.register(Payment, PaymentAdmin)
admin.site.register(StripeAccount, StripeAccountAdmin)
admin.site.register(Coupon, CouponAdmin)
