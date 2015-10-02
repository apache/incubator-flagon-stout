from django.conf.urls import patterns, include, url
from xdata import views
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
admin.autodiscover()
		
urlpatterns = patterns('',
	# include urls for op_tasks and administration pages
    url(r'^tasking/', include('op_tasks.urls', namespace="op_tasks")),
    url(r'^experiment/', include('exp_portal.urls', namespace="exp_portal")),
    # url(r'^developer/', include('developer.urls', namespace="developer")),
    url(r'^user_feedback/', views.user_feedback_home, name='user_feedback_home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('uploads.urls')),
    url(r'^$', views.index, name='index'),    
    # (r'^contact/$', contact),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
