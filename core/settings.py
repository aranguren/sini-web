# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')
REFRESH_TOKEN_SECRET = config('REFRESH_TOKEN_SECRET', default='S#perS3crEt_1122')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
ALLOWED_HOSTS = ['localhost', '127.0.0.1', config('SERVER', default='127.0.0.1')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leaflet',
    'djgeojson',
    'sini',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_simplejwt',
    'api',
    'apps.home'  # Enable the inner home (home)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'sini'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': int(os.getenv('DB_PORT', 5432)),
        'USER': os.getenv('DB_USER','postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD','postgres'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
#############################################################

MEDIA_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MEDIA_ROOT = os.path.join(MEDIA_BASE_DIR, 'media')
MEDIA_URL = '/uploaded/'

##################################################
#LEAFLET CONFIG

LEAFLET_CONFIG = {
    #'DEFAULT_CENTER': (-12.033207, -77.044158),
    'TILES': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

    #'DEFAULT_PRECISION': 6,

  'DEFAULT_CENTER': (18.47186, -69.89232),
  'DEFAULT_ZOOM': 12,
  'MIN_ZOOM': 7,
  'MAX_ZOOM': 19,
  'RESET_VIEW' : False,

    'PLUGINS': {
        'forms': {
            'auto-include': True
        }
    }
}

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10

}



EMAIL_HOST =  os.getenv('DJANGO_EMAIL_HOST', 'sandbox.smtp.mailtrap.io')
EMAIL_HOST_USER =  os.getenv( 'DJANGO_EMAIL_HOST_USER' , '57446d8d1a6be2')
EMAIL_HOST_PASSWORD =  os.getenv( 'DJANGO_EMAIL_HOST_PASSWORD','9667bd5a798c11')
EMAIL_PORT = os.getenv( 'DJANGO_EMAIL_PORT', '2525')
EMAIL_USE_TLS = os.getenv( 'DJANGO_EMAIL_USE_TLS', 'False').lower() in ['true', '1', 'True'] 
EMAIL_USE_SSL =  os.getenv( 'DJANGO_EMAIL_USE_SSL', 'False').lower() in ['true', '1', 'True'] 
DEFAULT_FROM_EMAIL = os.getenv( 'DEFAULT_FROM_EMAIL', 'GeoNode <no-reply@geonode.org>')
PASSWORD_RESET_TIMEOUT = int(os.getenv( 'PASSWORD_RESET_TIMEOUT',  259200))

#DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
#DJANGO_EMAIL_HOST=sandbox.smtp.mailtrap.io
#DJANGO_EMAIL_PORT=2525
#DJANGO_EMAIL_HOST_USER=57446d8d1a6be2
#DJANGO_EMAIL_HOST_PASSWORD=9667bd5a798c11
#DJANGO_EMAIL_USE_TLS=False
#DJANGO_EMAIL_USE_SSL=False
#DEFAULT_FROM_EMAIL="GeoNode <no-reply@geonode.org>"