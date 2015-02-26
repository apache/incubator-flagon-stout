from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs

urlpatterns= patterns('',
	url(r'^status$', 'exp_portal.views.view_status', name='view_status'),
	url(r'^products$', 'exp_portal.views.view_products', name='view_products'),
	)