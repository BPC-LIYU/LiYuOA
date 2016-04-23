# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clouddisk', '0002_auto_20160423_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='clouddisk',
            name='user',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u4eba', to=settings.AUTH_USER_MODEL, help_text='\u79c1\u4eba\u4e91\u76d8', null=True),
        ),
    ]
