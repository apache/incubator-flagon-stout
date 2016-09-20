# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.conf.urls import patterns, url
from django.conf import settings
from django.contrib.staticfiles import views as vs
from developer import views

urlpatterns= patterns('',
	url(r'^$', views.home_page, name='home'),
	url(r'^status$', views.view_dev_status, name='view_dev_status'),
	url(r'^products$', views.view_dev_products, name='view_dev_products'),
	url(r'^submit$', views.submit_product, name='submit_product'),
	url(r'^newProduct$', views.newProduct, name='newProduct'),
    url(r'^product_comp$', views.product_comp, name='product_comp'),
	)