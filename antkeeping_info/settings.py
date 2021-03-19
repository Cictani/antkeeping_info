"""
Django settings for antkeeping_info project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    CORS_ORIGIN_WHITELIST=(list, []),
    PUBLIC_ROOT=(environ.Path, None),
    INTERNAL_IPS=(list, []),
    RECAPTCHA_FORCE=(bool, False)
)

root = environ.Path(__file__) - 2  # two folder back (/a/b/ - 2 = /)

# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = root()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
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
    'staff',
    'api',
    'crispy_forms',
    'django_bootstrap_breadcrumbs',
    'captcha',
    'taggit',
    'rest_framework',
    'corsheaders',
    'sorl.thumbnail',
    'tinymce',
]

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

ROOT_URLCONF = 'antkeeping_info.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root.path('templates/')],
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
    'default': env.db()
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

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


PUBLIC_ROOT = env('PUBLIC_ROOT')
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(root.path('global_static/')),
]
STATIC_ROOT = ''

MEDIA_URL = '/media/'
MEDIA_ROOT = ''

if PUBLIC_ROOT is not None:
    STATIC_ROOT = PUBLIC_ROOT('static/')
    MEDIA_ROOT = PUBLIC_ROOT('media/')

# Django breadcrumbs
BREADCRUMBS_TEMPLATE = "django_bootstrap_breadcrumbs/bootstrap4.html"

# Crispy forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_URL = '/users/login'

# Bing api key
BING_API_KEY_SERVER = env('BING_API_KEY_SERVER')
BING_API_KEY_CLIENT = env('BING_API_KEY_CLIENT')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'home'

# Google Recaptcha
RECAPTCHA_FORCE = env('RECAPTCHA_FORCE')
RECAPTCHA_ENABLED = (not DEBUG) or RECAPTCHA_FORCE
if RECAPTCHA_ENABLED:
    RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/min',
        'user': '60/min'
    }
}

# Cors

CORS_ORIGIN_WHITELIST = env('CORS_ORIGIN_WHITELIST')

INTERNAL_IPS = env('INTERNAL_IPS')

CACHES = {
    'default': env.cache()
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'AKI'

# Email

EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

# prod settings

if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

SECURE_REFERRER_POLICY = 'origin-when-cross-origin'

# logging

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[{levelname}] {asctime} - {module} - {process:d} - '
                          '{thread:d} - {message}',
                'style': '{',
            },
            'simple': {
                'format': '[{levelname}] {asctime} - {module} - {message}',
                'style': '{',
            },
        },
        'handlers': {
            'file': {
                'level': 'WARNING',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': env('LOGGING_FILENAME'),
                'maxBytes': 1024 * 1024 * 10,  # 10MB
                'backupCount': 20,
                'formatter': 'simple'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'WARNING',
                'propagate': True,
            },
        },
    }
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_TIMEZONE = 'Europe/Berlin'

THUMBNAIL_QUALITY = 80

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}
