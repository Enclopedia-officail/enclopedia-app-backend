from django.contrib import admin
from .models import Coupon, Issuing, Invitation, InvitationCode

# Register your models here.

class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'amount_off', 'created_at', 'currency', 'duration', 'duration_in_month', 'max_redemptions', 'name', 'percent_off', 'times_redeemed', 'redeem_by')
    search_fields = ['id',]

class IssuingAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'duration', 'is_used', 'expiration')


admin.site.register(Coupon, CouponAdmin)
admin.site.register(Issuing, IssuingAdmin)
admin.site.register(Invitation)
admin.site.register(InvitationCode)