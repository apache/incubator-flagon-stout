from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs
from op_tasks.views import task_list, product, register, login_participant, logout_participant, intro, login_intro

urlpatterns = patterns('',
    # ex: /op_tasks/
    # url(r'^$', index, name='index'),
    url(r'^task_list/$', task_list, name='task_list'),
    url(r'^product/(?P<seq_pk>[0-9]+)$', product, name='product'),
    url(r'^register/$', register),
    url(r'^login/$', login_participant),
    url(r'^logout/$', logout_participant),
    url(r'^intro/$', intro),
    url(r'^login_intro/$', login_intro),
)

print settings.DEBUG, settings.STATIC_ROOT
if settings.DEBUG:
    urlpatterns += url(r'^static/(?P<path>.*)$', vs.serve),