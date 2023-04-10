import datetime
import os

from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

CORE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_celery_results',
    'django_celery_beat'
]

LOCAL_APPS = [
    'users',
    'innotwits',
]

INSTALLED_APPS = CORE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

CORE_MIDDLEWARES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CUSTOM_MIDDLEWARES = [
    'users.middleware.JWTAuthenticationMiddleware',
]

MIDDLEWARE = CORE_MIDDLEWARES + CUSTOM_MIDDLEWARES

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

JWT_AUTH = {
    'JWT_VERIFY': os.getenv('JWT_VERIFY'),
    'JWT_VERIFY_EXPIRATION': os.getenv('JWT_VERIFY_EXPIRATION'),
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=float(os.getenv('JWT_EXPIRATION_DELTA'))),
    'JWT_AUTH_HEADER_PREFIX': os.getenv('JWT_AUTH_HEADER_PREFIX'),
    'SIGNING_KEY': os.getenv('SECRET_KEY'),
    'ALGORITHM': os.getenv('JWT_ALGORITHM'),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.JWTAuthentication',
    ),
}

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_ENABLED = True

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Warsaw'
CELERY_TASK_TRACK_STARTED = True

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = os.getenv('AWS_SES_REGION_NAME')
AWS_SES_REGION_ENDPOINT = os.getenv('AWS_SES_REGION_ENDPOINT')
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')

AWS_STORAGE_BUCKET_NAME = 'innoter-yauhen'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_DEFAULT_ACL = 'public-read'

DEFAULT_FILE_STORAGE = 'core.storages.MediaStore'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CELERY_BEAT_SCHEDULE = {
    "scheduled_task": {
        "task": "innotwits.tasks.unblock_page",
        "schedule": crontab(minute=0, hour=0),
    }
}
