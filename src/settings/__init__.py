import os
import sys

from .apps import *
from .databases import *
from .logging import *

BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ov695n#ol+qtp^2_&zfi9o93w(#6ej*o2b!r4!j2d-u+j%92rl'
# SECURITY WARNING: don't run with debug turned on in production!
FIELD_ENCRYPTION_KEY = 'eP1DLk6t3mL2ZAmtAaInP5Mrbfza3dDXLNiwAhKbfxo='


ALLOWED_HOSTS = ['*']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

ROOT_URLCONF = 'urls'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

APPEND_SLASH = False

WSGI_APPLICATION = 'wsgi.application'

LANGUAGE_CODE = 'en'
LANGUAGE_CODES = [
    ('ru', 'Руский'),
    ('en', 'English')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, '../', 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'


LOCK_DIR = '/var/lock'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_COOKIE_AGE = 86400
SESSION_SAVE_EVERY_REQUEST = True

AUTH_USER_MODEL = 'account_system.User'

AUTHENTICATION_BACKENDS = [
    'account_system.backends.PhoneNumberBackend',
]