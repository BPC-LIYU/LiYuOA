# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liyu_organization', '0003_auto_20160426_1945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='members',
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='liyu_organization.Person', verbose_name='\u5206\u7ec4\u6210\u5458'),
        ),
    ]
