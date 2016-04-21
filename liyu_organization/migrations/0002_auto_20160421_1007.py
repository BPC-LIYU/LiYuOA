# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('liyu_organization', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liyuoa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectapply',
            name='user',
            field=models.ForeignKey(verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='person',
            name='org',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5e\u7ec4\u7ec7', to='liyu_organization.Organization'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.ForeignKey(verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='permissions',
            name='app',
            field=models.ForeignKey(verbose_name='\u5e94\u7528', to='liyuoa.AppInfo'),
        ),
        migrations.AddField(
            model_name='permissions',
            name='org',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5e\u7ec4\u7ec7', to='liyu_organization.Organization'),
        ),
        migrations.AddField(
            model_name='permissions',
            name='person',
            field=models.ForeignKey(verbose_name='\u7528\u6237', to='liyu_organization.Person'),
        ),
        migrations.AddField(
            model_name='permissions',
            name='role',
            field=models.ForeignKey(verbose_name='\u5e94\u7528', to='liyuoa.AppRole'),
        ),
        migrations.AddField(
            model_name='orgapp',
            name='app',
            field=models.ForeignKey(verbose_name='\u5e94\u7528', to='liyuoa.AppInfo'),
        ),
        migrations.AddField(
            model_name='orgapp',
            name='org',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5e\u7ec4\u7ec7', to='liyu_organization.Organization'),
        ),
        migrations.AddField(
            model_name='group',
            name='aide',
            field=models.ForeignKey(related_name='group_aide', verbose_name='\u52a9\u624b', to='liyu_organization.Person', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='charge',
            field=models.ForeignKey(related_name='group_charge', verbose_name='\u8d1f\u8d23\u4eba', to='liyu_organization.Person', null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ForeignKey(verbose_name='\u5206\u7ec4\u6210\u5458', to='liyu_organization.Person'),
        ),
        migrations.AddField(
            model_name='group',
            name='org',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5e\u7ec4\u7ec7', to='liyu_organization.Organization'),
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5e\u5173\u7cfb', to='liyu_organization.Group', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='permissions',
            unique_together=set([('org', 'person', 'app')]),
        ),
    ]
