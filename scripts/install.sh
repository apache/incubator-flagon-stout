#!/usr/bin/env bash

sudo yum -y install httpd

sudo chkconfig httpd on
sudo /etc/init.d/httpd start
