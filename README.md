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