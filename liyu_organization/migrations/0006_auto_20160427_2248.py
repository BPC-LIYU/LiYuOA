# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liyu_organization', '0005_auto_20160427_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='title',
            field=models.CharField(max_length=10, verbose_name='\u804c\u52a1', blank=True),
        ),
    ]
