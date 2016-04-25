# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('nsbcs', '0001_initial'),
        ('liyuoa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appapicomment',
            name='attachments',
            field=models.ManyToManyField(to='nsbcs.NsFile', verbose_name='\u9644\u4ef6'),
        ),
        migrations.AddField(
            model_name='appapicomment',
            name='to_comment',
            field=models.ForeignKey(verbose_name='\u7236\u7ea7\u8bc4\u8bba', to='liyuoa.AppApiComment', null=True),
        ),
        migrations.AddField(
            model_name='appapicomment',
            name='to_user',
            field=models.ForeignKey(related_name='api_to_comment', verbose_name='\u96b6\u5c5e\u7528\u6237', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='appapicomment',
            name='user',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5e\u7528\u6237', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='appapicareuser',
            name='api',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5eapi', to='liyuoa.AppApi'),
        ),
        migrations.AddField(
            model_name='appapicareuser',
            name='user',
            field=models.ForeignKey(verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appapi',
            name='app',
            field=models.ForeignKey(verbose_name='\u5e94\u7528', to='liyuoa.AppInfo', null=True),
        ),
        migrations.AddField(
            model_name='lyuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='lyuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='approle',
            unique_together=set([('role', 'app')]),
        ),
    ]
