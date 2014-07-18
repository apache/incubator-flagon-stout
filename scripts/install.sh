#!/usr/bin/env bash

sudo yum -y install httpd

sudo chkconfig httpd on
sudo /etc/init.d/httpd start

sudo yum -y install mod_wsgi
sudo yum -y install vim
