#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午8:44
# file:appinfo_sync_tools.py
# Email: wangjian2254@icloud.com
# Author: 王健
from django.conf import settings
from django.db import models

# Create your models here.
from util.basemodel import BaseModel


class CloudDisk(BaseModel):
    """
    云盘数据库
    by:王健 at:2016-04-20
    """
    name = models.CharField(max_length=50, verbose_name=u'磁盘目录')
    org = models.ForeignKey('liyu_organization.Organization', null=True, verbose_name=u'隶属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=u'所属人', help_text=u'私人云盘')
    is_pub = models.BooleanField(default=False, verbose_name=u'是否公共目录')
    group = models.ForeignKey('liyu_organization.Group', null=True, verbose_name=u'组织结构')
    father = models.ForeignKey('CloudDisk', null=True, verbose_name=u'父级目录')
    disk_type = models.IntegerField(default=0, verbose_name=u'目录类型', help_text=u'0:项目目录，1:个人目录')

    class Meta:
        list_json = ['name', 'is_pub', 'id', 'org_id', 'user_id', 'father_id', 'disk_type']
        detail_json = ['user_id', 'create_time', 'is_active']
