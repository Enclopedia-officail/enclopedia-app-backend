from django.apps import AppConfig

class NontificationConfig(AppConfig):
    name='notification'

    def ready(self):
        import notification.signalss
