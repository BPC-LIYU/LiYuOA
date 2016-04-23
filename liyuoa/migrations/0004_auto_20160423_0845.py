# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.basemodel


class Migration(migrations.Migration):

    dependencies = [
        ('liyuoa', '0003_appapiparameter_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppApiResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('name', models.CharField(max_length=30, verbose_name='\u5b57\u6bb5\u540d', db_index=True)),
                ('title', models.CharField(max_length=20, verbose_name='\u5b57\u6bb5\u4e2d\u6587\u540d')),
                ('desc', models.CharField(max_length=100, verbose_name='\u5b57\u6bb5\u5907\u6ce8')),
                ('value_type', models.CharField(max_length=10, verbose_name='\u6570\u503c\u7c7b\u578b')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
            ],
            options={
                'list_json': ['name', 'title', 'id', 'value_type', 'update_time', 'api_id', 'desc'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.AddField(
            model_name='appapi',
            name='response_type',
            field=models.CharField(default=b'', max_length=10, verbose_name='\u8fd4\u56de\u503c\u7c7b\u578b', blank=True),
        ),
        migrations.AlterField(
            model_name='appapiparameter',
            name='default',
            field=models.CharField(max_length=30, null=True, verbose_name='\u53c2\u6570\u9ed8\u8ba4\u503c'),
        ),
        migrations.AlterField(
            model_name='appinfo',
            name='namespace',
            field=models.CharField(db_index=True, max_length=20, verbose_name='\u6a21\u5757\u540d', blank=True),
        ),
        migrations.AddField(
            model_name='appapiresponse',
            name='api',
            field=models.ForeignKey(verbose_name='\u96b6\u5c5eapi', to='liyuoa.AppApi'),
        ),
    ]
