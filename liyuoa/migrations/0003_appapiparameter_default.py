# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liyuoa', '0002_auto_20160421_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='appapiparameter',
            name='default',
            field=models.CharField(max_length=30, null=True, verbose_name='\u53c2\u6570\u5907\u6ce8'),
        ),
    ]
