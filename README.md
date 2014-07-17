# Documentation for the XDATA Online Experiment

Once this package is cloned, create the database

```bash
$ python manage.py syncdb
```

This will also create a superuser.


# During development, if you want to drop to the database and start over run the following:

```bash
$ python manage.py sqlclear op_tasks | python manage.py dbshell
$ python manage.py syncdb
$ python manage.py populate_db
```

This will keep your super user and drop just the app database which is a lot nicer than deleting the whole database and starting over

This process is also under the `reset_optask` command

```bash
$ python manage.py reset_optask
```


# Getting this working on Vagrant

Get a base centos box (this may take awhile)
```bash
vagrant box add centos_6.5 https://github.com/2creatives/vagrant-centos/releases/download/v6.5.3/centos65-x86_64-20140116.box
```

Initialize Vagrantfile
```bash
vagrant init centos_6.5
```

Start it
```bash
vagrant up
```