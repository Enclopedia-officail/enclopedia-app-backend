# 本番環境用のsettings.py
from .base import *

DEBUG = False

CORS_ORIGIN_WHITELIST = (
    "https://www.enclopedia-official.com"
)
CSRF_TRUSTED_ORIGINS = ['https://api.enclopedia-official.com']

SITE_ID = 2

SENDGRID_SANDBOX_MODE_IN_DEBUG = False

#aws s3 setting
AWS_S3_REGION_NAME='ap-northeast-1'
AWS_STORAGE_BUCKET_NAME=env("AWS_BUCKET_NAME")
AWS_ACCESS_KEY_ID = env("AWS_PUBLIC_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY_ID = env("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = 'media.enclopedia-official.com'
#static
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#media
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_ROOT = 'https://%s/%s/' % ('media.enclopedia-official.com', PUBLIC_MEDIA_LOCATION)
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'backend.storage_backends.MediaStorage'
#csv
PUBLIC_CSV_LOCATION = 'csv'
CSV_URL = '/csv/'
CSV_ROOT = 'https://%s/%s/' % ('media.enclopedia-official.com', PUBLIC_CSV_LOCATION)

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