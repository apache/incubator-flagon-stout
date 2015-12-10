"""
Django settings for xdata project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from secret import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "op_tasks"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = MY_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# ADMINS = ADMIN_EMAILS

ALLOWED_HOSTS = ['*']

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

SITE_ID = 1

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)
# Application definition

INSTALLED_APPS = (
    'custom_user',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'op_tasks',
    'exp_portal',
    'developer',
    'uploads',
    'axes',  # Throttling capabilities
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.FailedLoginMiddleware',
)

ROOT_URLCONF = 'xdata.urls'

WSGI_APPLICATION = 'xdata.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    )

AUTH_USER_MODEL = 'custom_user.EmailUser'

# AUTH_PROFILE_MODULE = 'op_tasks.UserProfile'
# AUTH_USER_MODEL = 'op_tasks.MyUser'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
   #'default': {
   #    'ENGINE': 'django.db.backends.sqlite3',
   #    'NAME': os.path.join(BASE_DIR, '../db', 'db.sqlite3'),
   #}

     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'xdatadb',
         'USER': 'xdatauser',
         'PASSWORD': 'Dr@perUs3r!',
         'HOST': 'localhost', #'127.0.0.1',   # Or an IP Address that your DB is hosted on
         'PORT': '3306',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# STATIC_ROOT = "/var/www/html/stout/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '../static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = '/tasking/login'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Email integration setup
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAJJDM2ZC67STGF4IA'
EMAIL_HOST_PASSWORD = MY_EMAIL_PASSWORD

# Configurable email addresses
# These are addresses where mail is sent from...
EMAIL_FROM_NOMINAL_ADDRESS = "onlinetesting@xdataonline.com"
EMAIL_FROM_ERROR_ADDRESS = "no-reply@xdataonline.com"
# These are addresses used to send mail to...
EMAIL_TO_ERROR_ADDRESS = "errors@xdataonline.com"

# After three failed logins, require users to wait 5 minutes before they can attempt to log in again
AXES_LOGIN_FAILURE_LIMIT = 3
from datetime import timedelta
AXES_COOLOFF_TIME=timedelta(seconds = 300)

# Activity Logging Endpoint
ALE_URL = 'http://52.20.48.202'
