# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.basemodel


class Migration(migrations.Migration):

    dependencies = [
        ('liyu_organization', '0007_orgheadicon'),
        ('nsbcs', '0002_auto_20160429_0956'),
        ('clouddisk', '0003_clouddisk_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('clouddisk', models.ForeignKey(verbose_name='\u96b6\u5c5e\u4e91\u76d8', to='clouddisk.CloudDisk')),
                ('nsfile', models.ForeignKey(verbose_name='\u4e91\u6587\u4ef6', to='nsbcs.NsFile')),
                ('person', models.ForeignKey(verbose_name='\u96b6\u5c5e\u7ec4\u7ec7\u6210\u5458', to='liyu_organization.Person', null=True)),
            ],
            options={
                'list_json': ['id', 'person__user_id', 'nsfile_id', 'nsfile__name', 'nsfile__filetype', 'nsfile__size', 'nsfile__fileurl', 'nsfile__bucket', 'clouddisk_id'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
    ]
