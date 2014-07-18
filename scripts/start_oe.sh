#!/usr/bin/env bash

sudo cat /vagrant/files/httpd.conf >> /etc/httpd/conf/httpd.conf

mkdir /var/www/op_task

# sudo chmod -R 755 /var/www/op_task
sudo chown -R vagrant:vagrant /var/www/op_task

cp -r /vagrant/* /var/www/op_task

sudo rm -rf /var/www/op_task/db
sudo mkdir /var/www/op_task/db


sudo /etc/init.d/httpd restart

cd /var/www/op_task

printf "no\n" | python manage.py syncdb

sudo chown -R apache:apache /var/www/op_task/db
python manage.py populate_db