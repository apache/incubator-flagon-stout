from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs
from exp_portal import views

urlpatterns= patterns('',
	url(r'^$', views.home_page, name='home'),
	url(r'^status$', views.view_status, name='view_status'),
	url(r'^products$', views.view_products, name='view_products'),
	url(r'^products/manage$', views.manage_products, name='manage_products'),
	url(r'^tasks$', views.view_tasks, name='view_tasks'),
	url(r'^tasks/add$', views.add_task, name='add_task'),
	url(r'^tasks/new$', views.new_task, name='new_task'),
	url(r'^tasks/created$', views.task_added, name='task_added'),
	url(r'^tasks/completed$', views.view_completed, name='view_completed'), 
	url(r'^tasks/incomplete$', views.view_incomplete, name='view_incomplete'),
	url(r'^tasks/manage$', views.manage_tasks, name='manage_tasks'),
	url(r'^users$', views.view_users, name='view_users'), 
	url(r'^users/manage$', views.manage_users, name='manage_users'),
	url(r'^users/add$', views.add_user, name='add_user'),
	url(r'^users/new$', views.new_user, name='new_user'),
	url(r'^users/created$', views.user_added, name='user_added'),
	url(r'^users/tasks/add$', views.add_user_task, name='add_user_task'),
	url(r'^users/tasks/viewall/(?P<profile>.*)$', views.view_user_tasks, name='view_user_tasks'),
	url(r'^experiments/manage$', views.manage_exps, name='manage_exps'),
	)