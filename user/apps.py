from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccountConfig(AppConfig):
    name = 'user'

    def ready(self):
        from . import signals
