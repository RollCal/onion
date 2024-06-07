import sentry_sdk
from datetime import timedelta
from pathlib import Path
from .config import (_SECRET_KEY,
                     _POSTGRES_SETTING,
                     _REDIS_SETTING,
                     _EMBEDDING_HOST,
                     _EMAIL_HOST_USER,
                     _EMAIL_HOST_PASSWORD,
                     _SENTRY_DSN)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = _SECRET_KEY

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "www.onion-pi.com",
    "3.36.148.220",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.postgres',
    'django_celery_results',
    'django_celery_beat',

    'accounts',
    'onions',
    'profiles',
    'votes',
    'management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OpinionProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'onions/data_management/templates']
        ,
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

WSGI_APPLICATION = 'OpinionProject.wsgi.application'


AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=180),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# "DEVELOPMENT" OR "DEPLOYMENT"
DB_ENVIRONMENT = "DEVELOPMENT"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': _POSTGRES_SETTING[DB_ENVIRONMENT]["NAME"],
        'USER': _POSTGRES_SETTING[DB_ENVIRONMENT]["USER"],
        'PASSWORD': _POSTGRES_SETTING[DB_ENVIRONMENT]["PASSWORD"],
        'HOST': _POSTGRES_SETTING['HOST'],
        'PORT': _POSTGRES_SETTING[DB_ENVIRONMENT]["PORT"],
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{_REDIS_SETTING['HOST']}:{_REDIS_SETTING['PORT']}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CELERY_BROKER_URL = f"redis://{_REDIS_SETTING['HOST']}:{_REDIS_SETTING['PORT']}/0"
CELERY_RESULT_BACKEND = f"redis://{_REDIS_SETTING['HOST']}:{_REDIS_SETTING['PORT']}/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = _EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = _EMAIL_HOST_PASSWORD

EMBEDDING_HOST = _EMBEDDING_HOST

sentry_sdk.init(
    dsn=_SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

CELERY_TIMEZONE = TIME_ZONE

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
