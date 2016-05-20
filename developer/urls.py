from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs
from developer import views

urlpatterns= patterns('',
	url(r'^$', views.home_page, name='home'),
	url(r'^dev_status$', views.view_dev_status, name='view_dev_status'),
	url(r'^products$', views.view_dev_products, name='view_dev_products'),
	url(r'^submit$', views.submit_product, name='submit_product'),
	url(r'^newProduct$', views.newProduct, name='newProduct'),
    url(r'^product_comp$', views.product_comp, name='product_comp'),
	)
