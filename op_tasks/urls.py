from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs
from op_tasks import views 

urlpatterns = patterns('',
    # ex: /op_tasks/
    # url(r'^$', index, name='index'),
    url(r'^task_list/$', views.task_list, name='task_list'),
    url(r'^product/(?P<task_pk>[0-9]+)$', views.product, name='product'),
    url(r'^register$', views.register, name='register'),
    # url(r'^login/(?P<title>\w+)$', views.login_participant, name='login'),
    url(r'^login/$', views.login_participant, name='login'),
    url(r'^logout/$', views.logout_participant, name='logout'),
    url(r'^intro/$', views.intro, name='intro'),
    url(r'^intro/(?P<process>\w+)$', views.intro, name='intro'),
    url(r'^instruct/$', views.instruct, name='instruct'),
    url(r'^instruct/(?P<read>\w+)$', views.instruct, name='instruct'),
    url(r'^experiment_instructions$', views.exp_instruct, name='exp_instruct'),
    url(r'^portal_instructions$', views.portal_instruct, name='portal_instruct'),
    url(r'^product_instructions$', views.product_instruct, name='product_instruct'), 
    url(r'^user_profile$', views.view_profile, name='view_profile'), 
)

# print settings.DEBUG, settings.STATIC_ROOT
if settings.DEBUG:
    urlpatterns += url(r'^static/(?P<path>.*)$', vs.serve),