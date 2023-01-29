from datetime import timedelta
from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration
import environ
import yaml
import sentry_sdk
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['https://api.enclopedia-official.com', 'https://www.enclopedia-official.com']
CSRF_TRUSTED_ORIGINS = ['https://api.enclopedia-official.com']

# STRIPE API KEY
STRIPE_PUBLIC_KEY = env("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")
STRIPE_LIVE_MODE = False
STRIPE_API_VERSION = ['2020-08-27']
DJSTRIPE_WEBHOOK_SECRET = "whsec_xxx"

# google social login
SOCIAL_AUTH_GOOGLE_KEY = env('SOCIAL_AUTH_GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_SECRET = env('SOCIAL_AUTH_GOOGLE_SECRET')

GOOGLE_KEY_FILE_LOCATION = env('KEY_FILE_LOCATION')
GOOGLE_TRAKING_ID = env('GOOGLE_TRAKING_ID')

# Application definition
# debugツールバーは開発環境のみに使用
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    #'rest_framework_simplejwt.token_blacklist',
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'dj_rest_auth.registration',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'analytics',
    'category',
    'user.apps.AccountConfig',
    'product',
    'corsheaders',
    'reservation',
    'social_login',
    'subscription',
    'account_history',
    'dbbackup',
    'django_rest_passwordreset',
    # 'axes',pytho
    'debug_toolbar',
    'closet',
    'cart',
    'notification',
    'django_cleanup',
    'storages',
    'inventory',
    'buying'
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'PROVIDER_KEY': env('SOCIAL_AUTH_GOOGLE_KEY'),
        'PROVIDER_SECRET_KEY': env('SOCIAL_AUTH_GOOGLE_SECRET'),
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# usernameでの認証をemailを使用した認証に切り替える
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False

REST_USE_JWT = True

SITE_ID = 2

# debug_toolbarはテスト環境のみ適用
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'axes.middleware.AxesMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# debug_toolbarはテスト環境のみ適用
INTERNAL_IPS = ['127.0.0.1']

# debug_toolbarはテスト環境のみ適用
"""
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
"""


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    #apiポイントテンプレートを表示しないようにする設定
    #'DEFAULT_RENDERER_CLASSES': (
        #'rest_framework.renderers.JSONRenderer'
    #),
    'DEFAULT_PAGINATION_CLASS': 'backend.pagination.BasicPagination',
}

#celery related settigns
BROKER_URL = env('RABBITMQ_BROKER_URL')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/tokyo'

# ユーザー認証をカスタマイズする
"""
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
]
# ロックされるまでのログイン回数
AXES_FAILURE_LIIMT = 5
#ログイン解除にかかるまでの時間を指定
AXES_COOLOFF_TIME = 1
# ログインに成功したら失敗回数をリセットする
AXES_RESET_ON_SUCCESS = True
"""

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    # hs256の情報に関してはsimplejet state.pyで返される
    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    # jtiはこのtokenが一意の値であることを証明するために付与される
    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# 本番環境では書き換えが必要
CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://www.enclopedia-official.com"
)

CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT"
]
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "cookies"
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://"+ env('REDIS_LOCATION') +":6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

AUTH_USER_MODEL = 'user.Account'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# postgre RDSDATABASE

DATABASES = {
    'default':{
        'ENGINE': env("DB_ENGINE"),
        'NAME': env('DB_NAME'),
        'PASSWORD': env('DB_PASSWORD'),
        'USER': env('DB_USER'),
        'HOST': env('DB_HOST'),
        'PORT': env("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

SITE_ID = 7

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
CSV_URL = '/csv/'
CSV_ROOT = os.path.join(BASE_DIR, 'csv')

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'

DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'backups')}

# SMTP CONFIG
#send grid から送信する
SENDGRID_API_KEY = env('SENDGRID_API_KEY')
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER  = 'apikey'
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#debug modeでもsendgridから配信できるようにする
SENDGRID_SANDBOX_MODE_IN_DEBUG = False

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)

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