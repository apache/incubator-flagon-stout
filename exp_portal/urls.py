from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs

urlpatterns= patterns('',
	url(r'^$', 'exp_portal.views.home_page', name='home'),
	url(r'^status$', 'exp_portal.views.view_status', name='view_status'),
	url(r'^products$', 'exp_portal.views.view_products', name='view_products'),
	url(r'^submit$', 'exp_portal.views.submit_task', name='submit_task'),
	url(r'^newTask$', 'exp_portal.views.new_task', name='new_task'),
	url(r'^taskAdded$', 'exp_portal.views.task_added', name='task_added'),
	)