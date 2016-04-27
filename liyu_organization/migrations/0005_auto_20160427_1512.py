# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liyu_organization', '0004_auto_20160427_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissions',
            name='role',
            field=models.ForeignKey(verbose_name='\u5e94\u7528', to='liyuoa.AppRole', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='orgapp',
            unique_together=set([('org', 'app')]),
        ),
    ]
