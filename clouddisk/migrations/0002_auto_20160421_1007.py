# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liyu_organization', '0001_initial'),
        ('clouddisk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clouddisk',
            name='group',
            field=models.ForeignKey(verbose_name='\u7ec4\u7ec7\u7ed3\u6784', to='liyu_organization.Group', null=True),
        ),
        migrations.AddField(
            model_name='clouddisk',
            name='org',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5e\u9879\u76ee', to='liyu_organization.Organization', null=True),
        ),
    ]
