from django.conf.urls import patterns, include, url
from xdata.views import *
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()
		
urlpatterns = patterns('',
	# include urls for op_tasks and administration pages
    url(r'^op_tasks/', include('op_tasks.urls', namespace="op_tasks")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^exp_portal/exp_status$', 'exp_portal.views.view_status', name='view_status'),
    (r'^$', index),    
    (r'^contact/$', contact),

)

urlpatterns += staticfiles_urlpatterns()
