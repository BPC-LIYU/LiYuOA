# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.basemodel


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('name', models.CharField(max_length=30, verbose_name='\u5206\u7ec4\u540d\u79f0')),
                ('icon_url', models.URLField(null=True, verbose_name='\u56fe\u6807url')),
                ('sort', models.IntegerField(default=0, null=True, verbose_name='\u6392\u5e8f\u5b57\u6bb5', db_index=True)),
            ],
            options={
                'list_json': ['name', 'icon_url', 'id', 'org_id', 'is_active', 'sort', 'parent_id'],
                'detail_json': ['org__name', 'create_time', 'charge_id', 'charge__user_id', 'charge__realname', 'charge__user__icon_url', 'aide__realname', 'aide__user__icon_url', 'aide_id', 'aide__user_id'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('name', models.CharField(max_length=30, verbose_name='\u540d\u79f0')),
                ('icon_url', models.URLField(null=True, verbose_name='\u56fe\u6807url')),
            ],
            options={
                'list_json': ['name', 'icon_url', 'id'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='OrgApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('sort', models.IntegerField(default=0, null=True, verbose_name='\u6392\u5e8f\u5b57\u6bb5', db_index=True)),
            ],
            options={
                'list_json': ['org_id', 'app__name', 'id', 'sort', 'app__flag', 'app__typeflag'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
            ],
            options={
                'list_json': ['org_id', 'app__name', 'app__flag', 'app__typeflag', 'id', 'role__name', 'role_id'],
                'detail_json': ['create_time', 'is_active', 'person_id', 'person__user_id', 'person__realname', 'person__user__icon_url', 'role__role', 'role__desc'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('realname', models.CharField(max_length=8, verbose_name='\u771f\u5b9e\u59d3\u540d')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='\u7535\u5b50\u90ae\u4ef6')),
                ('title', models.CharField(max_length=10, verbose_name='\u804c\u52a1')),
                ('manage_type', models.IntegerField(default=0, help_text='0:\u666e\u901a\u7528\u6237;1\u666e\u901a\u7ba1\u7406\u54582:\u8d85\u7ea7\u7ba1\u7406\u5458;', verbose_name='\u8eab\u4efd\u7c7b\u578b', db_index=True)),
                ('is_gaoguan', models.BooleanField(default=False, verbose_name='\u9ad8\u7ba1\u6a21\u5f0f')),
                ('is_show_tel', models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a\u624b\u673a\u53f7')),
                ('is_show_email', models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a\u7535\u5b50\u90ae\u7bb1')),
            ],
            options={
                'list_json': ['realname', 'user__icon_url', 'id', 'user_id', 'org_id', 'title', 'manage_type', 'is_active'],
                'detail_json': ['user__realname', 'create_time', 'user__imusername', 'is_gaoguan', 'is_show_tel', 'is_show_email'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='ProjectApply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('content', models.CharField(max_length=100, verbose_name='\u7533\u8bf7')),
                ('status', models.NullBooleanField(default=None, help_text='None \u672a\u5904\u7406, True \u540c\u610f\uff0cFalse \u4e0d\u540c\u610f', verbose_name='\u662f\u5426\u540c\u610f', db_index=True)),
                ('checker', models.ForeignKey(related_name='checker', blank=True, to='liyu_organization.Person', help_text='\u96b6\u5c5e\u9879\u76ee', null=True, verbose_name='\u5ba1\u6838\u4eba')),
                ('org', models.ForeignKey(verbose_name='\u96b6\u5c5e\u7ec4\u7ec7', to='liyu_organization.Organization')),
            ],
            options={
                'list_json': ['user__realname', 'user__icon_url', 'id', 'org_id', 'status', 'content'],
                'detail_json': ['org__name', 'create_time', 'is_active', 'checker_id', 'checker__user_id', 'checker__user__icon_url', 'checker__realname'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
    ]
