"""
Django settings for xdata project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

from base import *

from secret import MY_ALE_URL

INSTALLED_APPS += (
    'django_extensions',
)

DEBUG = False
TEMPLATE_DEBUG = False

# Activity Logging Endpoint
ALE_URL = MY_ALE_URL
