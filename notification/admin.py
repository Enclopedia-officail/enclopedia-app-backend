from django.contrib import admin
from . import models
# Register your models here.

class ReadAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'read')
    list_per_page = 100
    search_fields = ['id', 'account__id']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',  'title')
    list_per_page = 100
    search_fields = ['id', 'user__id',   'title']

class  NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_per_page = 100
    search_fields = ['id', 'title']


admin.site.register(models.Read, ReadAdmin)
admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Todo)