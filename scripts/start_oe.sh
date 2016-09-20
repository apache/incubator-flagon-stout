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