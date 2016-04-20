# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LYUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('tel', models.CharField(max_length=20, unique=True, null=True, verbose_name='\u624b\u673a\u53f7')),
                ('icon_url', models.URLField(null=True, verbose_name='\u56fe\u6807url')),
                ('realname', models.CharField(help_text='\u771f\u5b9e\u59d3\u540d', max_length=8, null=True, verbose_name='\u771f\u5b9e\u59d3\u540d', blank=True)),
            ],
            options={
                'list_json': ['realname', 'icon_url', 'id'],
                'detail_json': ['username', 'email', 'tel', 'is_active', 'is_staff', 'date_joined'],
            },
        ),
        migrations.CreateModel(
            name='AppApi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('name', models.CharField(max_length=50, verbose_name='\u63a5\u53e3\u540d\u79f0', db_index=True)),
                ('url', models.CharField(unique=True, max_length=100, verbose_name='\u7edd\u5bf9url')),
                ('namespace', models.CharField(max_length=150, verbose_name='\u51fd\u6570\u76ee\u5f55', db_index=True)),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('code_content', models.TextField(verbose_name='\u4ee3\u7801')),
            ],
            options={
                'list_json': ['name', 'url', 'id', 'namespace'],
                'detail_json': ['create_time', 'is_active', 'code_content'],
            },
        ),
        migrations.CreateModel(
            name='AppApiCareUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('is_confirm', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5904\u7406\u8fc7')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
            ],
            options={
                'list_json': ['user_id', 'user__icon_url', 'id', 'user__realname', 'update_time', 'api_id', 'is_confirm'],
                'detail_json': ['create_time', 'is_active'],
            },
        ),
        migrations.CreateModel(
            name='AppApiParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('name', models.CharField(max_length=30, verbose_name='\u53c2\u6570\u540d', db_index=True)),
                ('title', models.CharField(max_length=20, verbose_name='\u53c2\u6570\u4e2d\u6587\u540d')),
                ('desc', models.CharField(max_length=100, verbose_name='\u53c2\u6570\u5907\u6ce8')),
                ('parm_type', models.CharField(max_length=10, verbose_name='\u53c2\u6570\u7c7b\u578b')),
                ('is_required', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5fc5\u987b')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
            ],
            options={
                'list_json': ['name', 'title', 'id', 'parm_type', 'is_required', 'update_time', 'api_id', 'desc'],
                'detail_json': ['create_time', 'is_active'],
            },
        ),
        migrations.CreateModel(
            name='AppApiReplay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('content', models.TextField(verbose_name='\u4fee\u6539\u5185\u5bb9,\u6216\u8bc4\u8bba\u5185\u5bb9')),
                ('username', models.CharField(max_length=30, verbose_name='\u533f\u540d\u6635\u79f0')),
                ('source', models.IntegerField(default=0, verbose_name='0:\u4fee\u6539\u6ce8\u91ca;1:\u6587\u6863\u81ea\u52a8\u5bf9\u6bd4;2:\u4eba\u5de5\u8bc4\u8bba')),
                ('api', models.ForeignKey(verbose_name='\u96b6\u5c5eapi', to='liyuoa.AppApi')),
            ],
            options={
                'list_json': ['content', 'user_id', 'id', 'api_id', 'user__realname', 'user__icon_url', 'to_user__realname', 'to_user__icon_url', 'create_time', 'to_replay_id', 'to_replay__content', 'to_replay__user_id', 'to_replay__user__icon_url', 'to_replay__user__realname', 'is_auto'],
                'detail_json': ['is_active'],
            },
        ),
        migrations.CreateModel(
            name='AppInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('flag', models.CharField(max_length=50, unique=True, null=True, verbose_name='\u529f\u80fd\u6807\u8bb0')),
                ('name', models.CharField(max_length=20, verbose_name='\u5e94\u7528\u540d\u79f0')),
                ('type_flag', models.CharField(max_length=20, verbose_name='\u5e94\u7528\u7c7b\u578b')),
                ('is_show', models.BooleanField(default=True, verbose_name='\u662f\u5426\u663e\u793a\u5728\u5e94\u7528\u5217\u8868')),
                ('desc', models.TextField(verbose_name='\u5e94\u7528\u63cf\u8ff0', blank=True)),
                ('namespace', models.CharField(db_index=True, max_length=20, verbose_name='\u5e94\u7528\u63cf\u8ff0', blank=True)),
            ],
            options={
                'list_json': ['flag', 'name', 'id', 'type_flag'],
                'detail_json': ['create_time', 'is_active', 'desc'],
            },
        ),
        migrations.CreateModel(
            name='AppRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, db_index=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u662f\u5426\u5220\u9664')),
                ('role', models.CharField(max_length=20, verbose_name='\u89d2\u8272')),
                ('name', models.CharField(max_length=20, verbose_name='\u89d2\u8272\u540d\u79f0')),
                ('desc', models.TextField(verbose_name='\u5e94\u7528\u63cf\u8ff0', blank=True)),
                ('app', models.ForeignKey(to='liyuoa.AppInfo')),
            ],
            options={
                'list_json': ['role', 'name', 'id', 'desc'],
                'detail_json': ['create_time', 'is_active'],
            },
        ),
    ]
