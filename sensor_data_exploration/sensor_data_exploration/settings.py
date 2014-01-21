"""
Django settings for sensor_data_exploration project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os




# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

PROJECT_DIR = os.path.dirname(__file__)
# parent directory
BASE_DIR = os.path.dirname(PROJECT_DIR + os.pardir)
# Absolute path, useful for templates
PROJECT_PATH = os.path.abspath(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6fi=sl-=r9fp!&5b2i$63fbzuy^kew^#k&!r%kw&gc!@^56sou'

# DEBUG is always false here.  Only turn it on in your local_settings.py file,
# which you DO NOT CHECK IN.  There should never be a local_settings.py on
# GitHub
DEBUG = False
TEMPLATE_DEBUG = False

# Application definition

DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
)

LOCAL_APPS = (
    'sensor_data_exploration.apps.explorer',
)

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sensor_data_exploration.urls'

WSGI_APPLICATION = 'sensor_data_exploration.wsgi.application'


# Database - commenting this out for Heroku
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# NOTE: This is for local development.  If we are on the production
# server, this DATABASES value is changed below.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# Templates
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashed, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

# Media page, for insecure storage of user data like uploaded profile pictures
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media') # absolute path

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

#Heroku specific
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Try to load local_settings.py if it exists
try:
    from local_settings import *
except Exception as e:
    pass
