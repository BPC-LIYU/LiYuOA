# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liyuim', '0004_auto_20160429_0956'),
        ('liyu_organization', '0007_orgheadicon'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='talkgroup',
            field=models.ForeignKey(verbose_name='\u90e8\u95e8\u7fa4', to='liyuim.TalkGroup', null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='liyu_organization.Person', verbose_name='\u90e8\u95e8\u6210\u5458'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=30, verbose_name='\u90e8\u95e8\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='orgheadicon',
            name='group',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5e\u90e8\u95e8', to='liyu_organization.Group', null=True),
        ),
    ]
