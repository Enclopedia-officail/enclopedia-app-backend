from django.apps import AppConfig


class BuyingConfig(AppConfig):
    name = 'buying'

    def ready(self):
        from . import signals
