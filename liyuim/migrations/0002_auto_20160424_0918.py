# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liyuim', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='is_muted',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u9759\u97f3'),
        ),
        migrations.AddField(
            model_name='talkuser',
            name='is_muted',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u9759\u97f3'),
        ),
    ]
