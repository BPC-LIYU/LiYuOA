# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.basemodel


class Migration(migrations.Migration):

    dependencies = [
        ('nsbcs', '0002_auto_20160429_0956'),
        ('liyu_organization', '0006_auto_20160427_2248'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgHeadIcon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('group', models.ForeignKey(verbose_name='\u96b6\u5c5e\u5206\u7ec4', to='liyu_organization.Group', null=True)),
                ('nsfile', models.ForeignKey(verbose_name='\u9644\u4ef6', to='nsbcs.NsFile')),
                ('org', models.ForeignKey(verbose_name='\u96b6\u5c5e\u7ec4\u7ec7', to='liyu_organization.Organization')),
                ('person', models.ForeignKey(verbose_name='\u4e0a\u4f20\u8005', to='liyu_organization.Person')),
            ],
            options={
                'list_json': ['id', 'org_id', 'group_id', 'person__user_id', 'nsfile_id', 'nsfile__name', 'nsfile__filetype', 'nsfile__size', 'nsfile__fileurl', 'nsfile__bucket'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
    ]
