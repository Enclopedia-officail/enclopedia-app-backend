from __future__ import absolute_import
from django.conf import settings
import os
from celery import Celery

import environ


env = environ.Env()
env.read_env(os.path.join(settings.BASE_DIR, '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend', broker=env("RABBITMQ_BROKER_URL"))
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()