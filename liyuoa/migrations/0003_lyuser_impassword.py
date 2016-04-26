# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('liyuoa', '0002_auto_20160423_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='lyuser',
            name='impassword',
            field=models.CharField(help_text='\u5373\u65f6\u901a\u4fe1\u8d26\u53f7\u5bc6\u7801', max_length=50, null=True, verbose_name='\u5373\u65f6\u901a\u4fe1\u8d26\u53f7\u5bc6\u7801'),
        ),
    ]
