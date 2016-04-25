# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liyuim', '0002_auto_20160424_0918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='talkapply',
            old_name='talk',
            new_name='talkgroup',
        ),
        migrations.RenameField(
            model_name='talkuser',
            old_name='read_tiemline',
            new_name='read_timeline',
        ),
        migrations.RenameField(
            model_name='talkuser',
            old_name='talk',
            new_name='talkgroup',
        ),
        migrations.AddField(
            model_name='talkgroup',
            name='is_add',
            field=models.BooleanField(default=True, verbose_name='\u6210\u5458\u662f\u5426\u53ef\u81ea\u7531\u52a0\u4eba'),
        ),
        migrations.AlterField(
            model_name='friend',
            name='is_muted',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u9759\u97f3'),
        ),
        migrations.AlterField(
            model_name='talkgroup',
            name='flag',
            field=models.CharField(max_length=50, verbose_name='\u7fa4\u6210\u5458md5', db_index=True),
        ),
        migrations.AlterField(
            model_name='talkuser',
            name='is_muted',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u9759\u97f3'),
        ),
        migrations.AlterUniqueTogether(
            name='friend',
            unique_together=set([('friend', 'owner')]),
        ),
    ]
