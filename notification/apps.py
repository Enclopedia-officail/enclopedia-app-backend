from ast import Import
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'

    def ready(self):
        try:
            from . import signals
        except ImportError:
            pass
