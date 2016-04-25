# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import util.basemodel
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('nsbcs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('nickname', models.CharField(max_length=30, verbose_name='\u597d\u53cb\u5907\u6ce8\u540d')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('is_black', models.BooleanField(default=False, verbose_name='\u662f\u5426\u9ed1\u540d\u5355')),
                ('friend', models.ForeignKey(verbose_name='\u597d\u53cb', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'list_json': ['user_id', 'user__realname', 'user__icon_url', 'nickname', 'id', 'owner_id', 'group_id', 'update_time'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='FriendApply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('status', models.IntegerField(default=0, help_text='0:\u672a\u5904\u7406,1:\u540c\u610f', verbose_name='\u72b6\u6001', db_index=True)),
                ('content', models.CharField(max_length=50, verbose_name='\u7533\u8bf7\u4fe1\u606f')),
                ('friend', models.ForeignKey(verbose_name='\u6536\u5230\u7533\u8bf7\u7684\u7528\u6237', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='friendapplyowner', verbose_name='\u53d1\u51fa\u7533\u8bf7\u7684\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'list_json': ['user_id', 'owner__realname', 'owner__icon_url', 'id', 'owner_id', 'content', 'create_time'],
                'detail_json': ['is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='FriendGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('name', models.CharField(max_length=20, verbose_name='\u5206\u7ec4\u540d\u79f0')),
                ('parent', models.ForeignKey(verbose_name='\u96b6\u5c5e\u5206\u7ec4', to='liyuim.FriendGroup', null=True)),
                ('user', models.ForeignKey(verbose_name='\u96b6\u5c5e\u7528\u6237', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'list_json': ['user_id', 'name', 'id', 'parent_id'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='IMFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('chat_id', models.IntegerField(verbose_name='\u53d1\u9001\u76ee\u6807', db_index=True)),
                ('is_group', models.BooleanField(default=False, db_index=True, verbose_name='\u662f\u5426\u53d1\u7ed9\u7fa4')),
                ('file_type', models.CharField(max_length=10, verbose_name='\u9644\u4ef6\u7c7b\u578b', db_index=True)),
                ('file', models.ForeignKey(verbose_name='\u9644\u4ef6', to='nsbcs.NsFile')),
            ],
            options={
                'list_json': ['id', 'chat_id', 'is_group', 'file_type', 'file_id', 'file__name', 'file__filetype', 'file__size'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='TalkApply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('status', models.IntegerField(default=0, help_text='0:\u672a\u5904\u7406,1:\u540c\u610f,2:\u62d2\u7edd', verbose_name='\u72b6\u6001', db_index=True)),
                ('content', models.CharField(max_length=50, verbose_name='\u7533\u8bf7\u4fe1\u606f')),
                ('reply', models.CharField(max_length=50, verbose_name='\u5904\u7406\u4fe1\u606f')),
            ],
            options={
                'list_json': ['id', 'talk_id', 'talk__icon_url', 'talk__name', 'status', 'content', 'reply', 'checker_id', 'checker__nickname', 'checker__user__icon_url'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='TalkGongGao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('content', models.TextField(verbose_name='\u516c\u544a\u5185\u5bb9')),
            ],
            options={
                'list_json': ['id', 'talk_id', 'tuser__nickname', 'tuser__user__icon_url', 'content'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='TalkGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('name', models.CharField(max_length=30, verbose_name='\u7fa4\u540d\u79f0')),
                ('max_member_count', models.IntegerField(default=100, verbose_name='\u6210\u5458\u6570\u9650\u5236')),
                ('group_type', models.IntegerField(default=0, help_text='0:\u666e\u901a\u7fa4;1:\u4f01\u4e1a\u7fa4;2:\u4f01\u4e1a\u90e8\u95e8;3:\u8ba8\u8bba\u7ec4', verbose_name='\u7fa4\u7c7b\u578b')),
                ('flag', models.CharField(max_length=50, verbose_name='\u7fa4\u6210\u5458md5')),
                ('icon_url', models.CharField(max_length=255, null=True, verbose_name='\u7fa4\u5934\u50cf')),
                ('owner', models.ForeignKey(verbose_name='\u7fa4\u4e3b', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'list_json': ['owner_id', 'owner__realname', 'owner__icon_url', 'name', 'id', 'member_num', 'group_type', 'icon_url'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.CreateModel(
            name='TalkUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('nickname', models.CharField(max_length=30, verbose_name='\u7fa4\u540d\u7247')),
                ('role', models.IntegerField(default=0, help_text='0:\u6210\u5458;1:\u7ba1\u7406\u5458;', verbose_name='\u7fa4\u89d2\u8272')),
                ('read_tiemline', models.IntegerField(default=0, verbose_name='\u5df2\u8bfb\u65f6\u95f4\u6233')),
                ('talk', models.ForeignKey(verbose_name='\u7fa4', to='liyuim.TalkGroup')),
                ('user', models.ForeignKey(verbose_name='\u7fa4\u6210\u5458', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'list_json': ['id', 'user__realname', 'user__icon_url', 'nickname', 'role', 'read_timeline'],
                'detail_json': ['create_time', 'is_active'],
            },
            bases=(models.Model, util.basemodel.JSONBaseMixin, util.basemodel.ModefyMixin),
        ),
        migrations.AddField(
            model_name='talkgonggao',
            name='talk',
            field=models.ForeignKey(verbose_name='\u7fa4', to='liyuim.TalkGroup'),
        ),
        migrations.AddField(
            model_name='talkgonggao',
            name='tuser',
            field=models.ForeignKey(verbose_name='\u53d1\u5e03\u4eba', to='liyuim.TalkUser'),
        ),
        migrations.AddField(
            model_name='talkapply',
            name='checker',
            field=models.ForeignKey(verbose_name='\u5904\u7406\u4eba', to='liyuim.TalkUser', null=True),
        ),
        migrations.AddField(
            model_name='talkapply',
            name='owner',
            field=models.ForeignKey(verbose_name='\u7533\u8bf7\u53d1\u51fa\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='talkapply',
            name='talk',
            field=models.ForeignKey(verbose_name='\u7533\u8bf7\u7fa4', to='liyuim.TalkGroup'),
        ),
        migrations.AddField(
            model_name='imfile',
            name='owner',
            field=models.ForeignKey(verbose_name='\u53d1\u9001\u8005', to='liyuim.TalkUser'),
        ),
        migrations.AddField(
            model_name='friend',
            name='group',
            field=models.ForeignKey(verbose_name='\u5206\u7ec4', to='liyuim.FriendGroup', help_text='\u6ca1\u5206\u7ec4\u7684\u5c31\u662f"\u6211\u7684\u597d\u53cb"\u5206\u7ec4,\u9ed8\u8ba4', null=True),
        ),
        migrations.AddField(
            model_name='friend',
            name='owner',
            field=models.ForeignKey(related_name='friendowner', verbose_name='\u597d\u53cb', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
