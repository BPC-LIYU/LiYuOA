# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liyuim', '0003_auto_20160425_1130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imfile',
            old_name='file',
            new_name='nsfile',
        ),
        migrations.RemoveField(
            model_name='imfile',
            name='chat_id',
        ),
        migrations.RemoveField(
            model_name='imfile',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='imfile',
            name='is_group',
        ),
        migrations.RemoveField(
            model_name='imfile',
            name='owner',
        ),
        migrations.AddField(
            model_name='imfile',
            name='chat_session',
            field=models.CharField(max_length=50, null=True, verbose_name='\u53d1\u9001\u7fa4', db_index=True),
        ),
        migrations.AddField(
            model_name='imfile',
            name='user',
            field=models.ForeignKey(verbose_name='\u53d1\u9001\u8005', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
