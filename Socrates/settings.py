"""
Django settings for Socrates project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import expanduser
from shutil import copyfile

from django.contrib import messages
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#5#2&!q%q7^i!oja+mpdamd-+m87ft3ki9+w3a=@8w)$80v*-q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "app.kotkt.nl",
    "localhost:8000",
    "localhost:7000"
]

DATE_INPUT_FORMATS = [
    "%d-%m-%Y",
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'crispy_forms',
    'account',
    'achievements',
    'debug_toolbar',
    'dining',
    'events',
    'news',
    'groups',
    'markdown_deux',
    'hijack',
    'compat',
    'api',
    'rest_framework',
    'corsheaders',
    'djoser',
    'silk',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware'
)

ROOT_URLCONF = 'Socrates.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'assets/templates')],
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

WSGI_APPLICATION = 'Socrates.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases



# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static_total")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets/static/'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"

# Crispy

CRISPY_TEMPLATE_PACK = "bootstrap3"

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger'
}

EMAIL_BACKEND = "sgbackend.SendGridBackend"

HIJACK_LOGIN_REDIRECT_URL = '/accounts/'  # Where admins are redirected to after hijacking a user
HIJACK_LOGOUT_REDIRECT_URL = '/admin/auth/user/'  # Where admins are redirected to after releasing a user

# CORS

CORS_ORIGIN_WHITELIST = (
    'app.kotkt.nl',
    'localhost:8000',
    'localhost:7000'
)

APPEND_SLASH = True

# Disable allowed host emails

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}

# Silky

SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

try:
    exec (open(expanduser(os.path.join(BASE_DIR + "/Socrates/config.py"))).read())
except:
    copyfile(expanduser(os.path.join(BASE_DIR + "/Socrates/config.sample.py")),
             expanduser(os.path.join(BASE_DIR + "/Socrates/config.py")))
    exec (open(expanduser(os.path.join(BASE_DIR + "/Socrates/config.py"))).read())
