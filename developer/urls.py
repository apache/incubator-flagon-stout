from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs

urlpatterns= patterns('',
	url(r'^$', 'developer.views.home_page', name='home'),
	url(r'^status$', 'developer.views.view_status', name='view_status'),
	url(r'^products$', 'developer.views.view_products', name='view_products'),
	url(r'^submit$', 'developer.views.submit_product', name='submit_product'),
	url(r'^newProduct$', 'developer.views.newProduct', name='newProduct'),
    url(r'^product_comp$', 'developer.views.product_comp', name='product_comp'),
	)