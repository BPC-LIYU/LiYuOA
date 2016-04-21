# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.basemodel


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CloudDisk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('name', models.CharField(max_length=50, verbose_name='\u78c1\u76d8\u76ee\u5f55')),
                ('is_pub', models.BooleanField(default=False, verbose_name='\u662f\u5426\u516c\u5171\u76ee\u5f55')),
                ('disk_type', models.IntegerField(default=0, help_text='0:\u9879\u76ee\u76ee\u5f55\uff0c1:\u4e2a\u4eba\u76ee\u5f55', verbose_name='\u76ee\u5f55\u7c7b\u578b')),
                ('father', models.ForeignKey(verbose_name='\u7236\u7ea7\u76ee\u5f55', to='clouddisk.CloudDisk', null=True)),
            ],
            options={
                'list_json': ['name', 'is_pub', 'id', 'org_id', 'user_id', 'father_id', 'disk_type'],
                'detail_json': ['user_id', 'create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
    ]
