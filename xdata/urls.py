from django.conf.urls import patterns, include, url
from xdata.views import *
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()
		
urlpatterns = patterns('',
	# include urls for op_tasks and administration pages
    url(r'^tasking/', include('op_tasks.urls', namespace="op_tasks")),
    url(r'^experiment/', include('exp_portal.urls', namespace="exp_portal")),
    url(r'^developer/', include('developer.urls', namespace="developer")),
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', index),    
    # (r'^contact/$', contact),

)

urlpatterns += staticfiles_urlpatterns()
