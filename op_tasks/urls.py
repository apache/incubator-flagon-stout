from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs
from op_tasks import views 

urlpatterns = patterns('',
    # ex: /op_tasks/
    # url(r'^$', index, name='index'),
    url(r'^task_list/$', views.task_list, name='task_list'),
    url(r'^product/(?P<task_pk>[0-9]+)$', views.product, name='product'),
    url(r'^product_test/(?P<task_pk>[0-9]+)$', views.product_test, name='product_test'),
    url(r'^task_test/(?P<task_pk>[0-9]+)$', views.task_test, name='task_test'),
    url(r'^task_launch/(?P<task_pk>[0-9]+)$', views.task_launch, name='task_launch'),
    url(r'^register$', views.register, name='register'),
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
    url(r'^reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.reset_confirm, name='reset_confirm'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^reset/sent/$', views.reset_sent, name='reset_sent'),
    url(r'^safety/$', views.safety, name='safety'),
)

# print settings.DEBUG, settings.STATIC_ROOT
if settings.DEBUG:
    urlpatterns += url(r'^static/(?P<path>.*)$', vs.serve),