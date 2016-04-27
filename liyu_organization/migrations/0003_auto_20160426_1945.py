# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.basemodel
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liyu_organization', '0002_auto_20160423_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgApply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('content', models.CharField(max_length=100, verbose_name='\u7533\u8bf7')),
                ('status', models.IntegerField(default=0, help_text='0:\u672a\u5904\u7406,1:\u540c\u610f,2:\u62d2\u7edd', verbose_name='\u72b6\u6001', db_index=True)),
                ('checker', models.ForeignKey(related_name='checker', blank=True, to='liyu_organization.Person', help_text='\u96b6\u5c5e\u9879\u76ee', null=True, verbose_name='\u5ba1\u6838\u4eba')),
                ('org', models.ForeignKey(verbose_name='\u96b6\u5c5e\u7ec4\u7ec7', to='liyu_organization.Organization')),
                ('user', models.ForeignKey(verbose_name='\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'list_json': ['user__realname', 'user__icon_url', 'id', 'org_id', 'status', 'content'],
                'detail_json': ['org__name', 'create_time', 'is_active', 'checker_id', 'checker__user_id', 'checker__user__icon_url', 'checker__realname'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.RemoveField(
            model_name='projectapply',
            name='checker',
        ),
        migrations.RemoveField(
            model_name='projectapply',
            name='org',
        ),
        migrations.RemoveField(
            model_name='projectapply',
            name='user',
        ),
        migrations.DeleteModel(
            name='ProjectApply',
        ),
    ]
