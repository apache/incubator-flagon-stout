# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='dirPath',
            field=models.CharField(default=b'abc', max_length=1000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to=models.CharField(default=b'abc', max_length=1000)),
        ),
    ]
