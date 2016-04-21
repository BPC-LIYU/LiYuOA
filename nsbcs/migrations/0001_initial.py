# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.basemodel
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('liyu_organization', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clouddisk', '0002_auto_20160421_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='NsFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('name', models.CharField(max_length=50, verbose_name='\u9644\u4ef6\u540d\u79f0')),
                ('fileurl', models.CharField(max_length=255, verbose_name='\u6587\u4ef6\u5b58\u50a8\u4f4d\u7f6e')),
                ('filetype', models.CharField(max_length=20, verbose_name='\u6587\u4ef6\u7c7b\u578b')),
                ('size', models.BigIntegerField(default=0, verbose_name='\u6587\u4ef6\u5927\u5c0f')),
                ('bucket', models.CharField(max_length=20, verbose_name='\u4f4d\u7f6e', blank=True)),
                ('group_type', models.IntegerField(default=0, db_index=True, choices=[(0, '\u7cfb\u7edf\u56fe\u7247'), (1, '\u7528\u6237\u56fe\u7247'), (3, '\u7ec4\u7ec7\u56fe\u7247')])),
                ('cloud_disk', models.ForeignKey(verbose_name='\u96b6\u5c5e\u4e91\u76d8\u76ee\u5f55', to='clouddisk.CloudDisk', null=True)),
                ('org', models.ForeignKey(verbose_name='\u96b6\u5c5e\u9879\u76ee', to='liyu_organization.Organization', help_text='\u96b6\u5c5e\u9879\u76ee', null=True)),
                ('person', models.ForeignKey(verbose_name='\u96b6\u5c5e\u7ec4\u7ec7\u6210\u5458', to='liyu_organization.Person', help_text='\u96b6\u5c5e\u9879\u76ee', null=True)),
                ('user', models.ForeignKey(verbose_name='\u4f5c\u8005', to=settings.AUTH_USER_MODEL, help_text='\u4e0a\u4f20\u4eba', null=True)),
            ],
            options={
                'list_json': ['name', 'fileurl', 'bucket', 'id', 'filetype', 'size', 'cloud_disk_id', 'group_type'],
                'detail_json': ['create_time', 'is_active', 'user_id', 'org_id', 'person_id', 'person__realname', 'person__user__icon_url', 'cloud_disk__name'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
    ]
