from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs
# from op_tasks.views import *

urlpatterns = patterns('',
    # ex: /op_tasks/
    # url(r'^$', index, name='index'),
    url(r'^task_list/$', op_tasks.views.task_list, name='task_list'),
    url(r'^product/(?P<seq_pk>[0-9]+)$', op_tasks.views.product, name='product'),
    url(r'^register/$', op_tasks.views.register),
    url(r'^login/$', op_tasks.views.login_participant),
    url(r'^logout/$', op_tasks.views.logout_participant),
    url(r'^intro/$', op_tasks.views.intro),
    url(r'^login_intro/$', op_tasks.views.login_intro),
    url(r'^instruct/$', op_tasks.views.instruct, name='instruct'),
)

print settings.DEBUG, settings.STATIC_ROOT
if settings.DEBUG:
    urlpatterns += url(r'^static/(?P<path>.*)$', vs.serve),