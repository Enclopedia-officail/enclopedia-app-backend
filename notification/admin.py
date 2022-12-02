from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Read)
admin.site.register(models.Notification)
admin.site.register(models.News)