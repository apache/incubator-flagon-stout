from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('uploads.views',
    url(r'^expuploads/$', 'expuploads', name='expuploads'),
)