from django.contrib import admin
from .models import Account, Profile, Adress, EmailSubscribe, RandomNumber, AuthPhoneNumber
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class AccountsAdmin(UserAdmin):
    """
    admin model
    """
    list_display = ('id', 'first_name', 'last_name', 'username', 'phone_number',
                    'email', 'data_joined', 'last_login', 'is_active')

    filter_horizontal = ()
    list_filter = []
    search_fields = ['email']
    fieldsets = ()


admin.site.register(Account, AccountsAdmin)
admin.site.register(Profile)
admin.site.register(Adress)
admin.site.register(EmailSubscribe)
admin.site.register(RandomNumber)
admin.site.register(AuthPhoneNumber)
