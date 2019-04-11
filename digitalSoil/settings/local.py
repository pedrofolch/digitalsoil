"""
Django settings for digitalSoil project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import dj_database_url
from .email_info import *
from digitalSoil.aws.conf import *


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fk($@02mfjzi-2n-iobu^vl=6sespv4ss_291)p9grvv4a3^va'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "digitalsoil.herokuapp.com", "0.0.0.0", "127.0.0.1"]


SEND_GRID_API_KEY = ''
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
EMAIL_USE_TLS = EMAIL_USE_TLS
DEFAULT_FROM_EMAIL = ''
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


ADMINS = (
    ('pedrofolch', 'pedro.folch@gmail.com')
)

MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'world',
    'comments',

    'corsheaders',
    'rest_framework',

    'django.contrib.sites',

    # added for allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'stripe',

    'accounts',
    'products',
    'shopping_cart',

    'memberships',
    'courses',

    'providers',
    'shops',

    'assets',
    'engine_room',
    'maintenance',
    'property',
    'personnel',

    'iotsensor',

    'posts',

    'fuel_station',
    'repairs',
    'purchase',

    'pages',
    'newsletter',
    'analytics',
    'videos',

    # from Soilfoodweb
    'recipes',
    'fieldwork',
    'labsoil',

    'crispy_forms',
    'markdown_deux',
    'pagedown',
    'storages',
    'webpack_loader',
    'graphene_django',

]

GRAPHENE = {
    'SCHEMA': 'digitalsoil.schema.schema'
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'digitalSoil.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'digitalSoil.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'digitalsoil',
        'USER': 'pedrofolch',
        'PASSWORD': '@Casairu1969',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'MST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/local/',  # end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats-local.json'),
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


VENV_PATH = os.path.dirname(BASE_DIR)

STATIC_ROOT = os.path.join(BASE_DIR, "live-static", "static-root")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "live-static", "media-root")

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'


# Stripe and Braintree Settings
if DEBUG:
    # test keys
    STRIPE_PUBLISHABLE_KEY = 'pk_test_cOcLydKwzzTdV1djWPHP0MgC'
    STRIPE_SECRET_KEY = 'sk_test_K1Dm7Vb674L4GBPtkTPkGzDx'
    BT_ENVIRONMENT = 'sandbox'
    BT_MERCHANT_ID = 'pgg678cpmhqn85sy'
    BT_PUBLIC_KEY = 'x5hyys9kzh54tpfk'
    BT_PRIVATE_KEY = 'b6655b1b4aa7500691cdc3d18a87c66a'
else:
    # live keys
    STRIPE_PUBLISHABLE_KEY = 'pk_test_cOcLydKwzzTdV1djWPHP0MgC'
    STRIPE_SECRET_KEY = 'sk_test_K1Dm7Vb674L4GBPtkTPkGzDx'


# Django AllAuth Settings

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

CORS_URLS_REGEX = r'^/api.*'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*',
    'digitalsoil.herokuapp.com',
    'projectdigitalsoil.s3-us-west-1.amazonaws.com',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    )
}
