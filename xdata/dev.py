"""
Django settings for xdata project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

from .base import *

INSTALLED_APPS += (
    'django_extensions',
)

DEBUG = True
TEMPLATE_DEBUG = True

# Activity Logging Endpoint
ALE_URL = 'http://127.0.0.1'
