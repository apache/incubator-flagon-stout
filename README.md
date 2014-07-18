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


# Getting this working on Vagrant (VirtualBox)

Get a base centos box (this may take awhile)
```bash
vagrant box add centos_6.5 https://github.com/2creatives/vagrant-centos/releases/download/v6.5.3/centos65-x86_64-20140116.box
```

Start it
```bash
vagrant up virtualbox
```

# Getting this working on Vagrant (OpenStack)

Get a base centos box (this may take awhile)

You need 2 files:

1. The first is the `.pem` (`.cer`) file which is the KeyPair file you can download from the OpenStack dashboard.

2. The second is a shell script which contains all the environment variables referenced in the Vagrantfile.  This is located under API Access under the Security Settings.  Once you download this file run `source $file.sh`, and this will ask you for you OpenStack password and load all the required varaibles under your current environment.  

Adjust the Vagrantfile to use the appropriate `.pem` file and the appropriate KeyPair name associated with that pem file.  Once that is complete you can run:

```bash
vagrant up openstack --provider=openstack
```