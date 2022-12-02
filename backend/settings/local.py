# local環境用のsettings.py
from .base import *

DEBUG = True

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS += ['debug_toolbar']


SITE_ID = 7

# debug_toolbarはテスト環境のみ適用

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# debug_toolbarはテスト環境のみ適用
INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

INSTALLED_APPS =+ [
    'debug_toolbar',
    'dbbackup',
]

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
)

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# SMTP CONFIG

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CSV_URL = '/csv/'
CSV_ROOT = os.path.join(BASE_DIR, 'csv')

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'

DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'backups')}

SENDGRID_SANDBOX_MODE_IN_DEBUG = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'fomrat': '[{asctime}] {levelname} {message}',
            'style': '{',
        },
    },

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }},

    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ['require_debug_true'],
            "class": "logging.StreamHandler",
            "formatter": 'simple',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            "formatter": 'simple',
            'formatter': 'simple',
        },
        "info_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "info.log"),
            "formatter": 'verbose',
        },
        'error_mail': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_true'],
            "formatter": 'verbose',
        }
    },
    'loggers': {
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagete': True,
        },
        'django.server':{
            'handlers': ['django.server'],
            'level': 'INFO',
            'progate': False,
        },
        'django.request': {
            'handlers':  ['error_mail', 'info_file'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}



# cookiewを使用した認証を実装する
