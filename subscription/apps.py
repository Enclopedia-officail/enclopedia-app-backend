from django.apps import AppConfig


class SubscriptionConfig(AppConfig):
    name = 'subscription'

    def ready(self):
        from .import signals
