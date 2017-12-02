# -*- coding:utf-8 -*-
"""
Django settings for cts project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jg=1oi+0)-ho-*rt!xpq)^c-w+zne_8d-mjo_2m(ov-2@pj6yg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# 允许跨域
CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # add
    'blog.apps.BlogConfig',
    'core.apps.CoreConfig',
    'crispy_forms',
    'rest_framework',  # rest_framework
    'django_filters'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_AUTHENTICATION_CLASS': (
        'rest_framework.authentication.TokenAuthentication',
        ),
}
STANDARD_PAGE_SIZE = 10

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 允许跨域
]

ROOT_URLCONF = 'cts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'cts.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/cts/static/'
MEDIA_URL = '/cts/media/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

###############################################
# dev settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cts',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': 3306
    }
}

LOGIN_URL = '/cts/login/'
LOGIN_REDIRECT_URL = '/cts/blog/'

STATIC_ROOT = '/var/www/cts/static/'
MEDIA_ROOT = '/var/www/cts/media/'
###############################################
LOPS_HOST = 'http://172.16.76.183'
LOPS_AUTH_API = os.path.join(LOPS_HOST, 'core/api/auth/token/')
LOPS_AUTH = True
LOPS_EMAIL_API = os.path.join(LOPS_HOST, 'core/api/email/')
LOPS_USER_DATA = os.path.join(LOPS_HOST, 'core/api/user/{username}/')
LOPS_AUTH_COOKIE = 'lops_token'
LOPS_LOGIN_URL = '/login/'
###############################################
# pro settings
CONFIG_FILE = '/etc/cts/cts.conf'
