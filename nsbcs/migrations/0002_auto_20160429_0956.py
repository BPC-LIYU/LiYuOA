# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nsbcs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nsfile',
            name='cloud_disk',
        ),
        migrations.RemoveField(
            model_name='nsfile',
            name='group_type',
        ),
        migrations.RemoveField(
            model_name='nsfile',
            name='org',
        ),
        migrations.RemoveField(
            model_name='nsfile',
            name='person',
        ),
        migrations.AddField(
            model_name='nsfile',
            name='access_type',
            field=models.CharField(default=b'public', max_length=10, db_index=True),
        ),
        migrations.AddField(
            model_name='nsfile',
            name='file_status',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
