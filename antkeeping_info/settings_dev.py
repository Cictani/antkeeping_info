"""
Django settings for antkeeping_info project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cmbu3krh0m@r6^6&motl4*q#p9+pm@v=9ko-z1&4dz^&e&$xg)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ants',
    'home',
    'regions',
    'flights',
    'users',
    'search',
    'crispy_forms',
    'django_bootstrap_breadcrumbs',
    'snowpenguin.django.recaptcha2',
    'cookielaw'
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

ROOT_URLCONF = 'antkeeping_info.urls'

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

WSGI_APPLICATION = 'antkeeping_info.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'antkeeping_info',
        'USER': 'antkeeping_info_user',
        'PASSWORD': ''
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
PASS_VALIDATION_MODULE = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': PASS_VALIDATION_MODULE + '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': PASS_VALIDATION_MODULE + '.MinimumLengthValidator',
    },
    {
        'NAME': PASS_VALIDATION_MODULE + '.CommonPasswordValidator',
    },
    {
        'NAME': PASS_VALIDATION_MODULE + '.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "global_static")
]

# Crispy forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Google api key
GOOGLE_API_KEY_SERVER = 'YOUR_KEY'
GOOGLE_API_KEY_CLIENT = 'YOUR_KEY'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'home'

# Google Recaptcha
RECAPTCHA_PUBLIC_KEY = 'YOUR_PUBLIC_KEY'
RECAPTCHA_PRIVATE_KEY = 'YOUR_PRIVATE_KEY'
