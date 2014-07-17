"""
Django settings for xdata project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "op_tasks"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^&q%n$=5vimv%q+9vzi#s62w8*1&w#(vb#dv0n0o6qnpa!l%m%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'op_tasks',
    # 'crispy_forms',
    # 'south'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'xdata.urls'

WSGI_APPLICATION = 'xdata.wsgi.application'



AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'op_tasks.models.MyBackend'
    )

# AUTH_PROFILE_MODULE = 'op_tasks.UserProfile'
# AUTH_USER_MODEL = 'op_tasks.MyUser'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'xdata',
    #     'USER': 'django',
    #     'PASSWORD': 'password',
    #     'HOST': 'localhost'
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': '/vagrant/db.sqlite3'
        # 'USER': 'django',
        # 'PASSWORD': 'password',
        # 'HOST': 'localhost'
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
# STATIC_ROOT = "/home/dreed/Projects/xdata/oe/static/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    # "/home/dft1618/xdata/oe/static/",
    # "/Users/dantraviglia/Desktop/Draper/xdata/oe061614/oe/static/"
)

LOGIN_URL = '/login/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'