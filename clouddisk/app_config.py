#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午7:27
# file:app_config.py
# Email: wangjian2254@icloud.com
# Author: 王健

# APP_NAMESPACE = 'liyu_organization'

AppCloudDiskName = u'云盘'


class AppCloudDisk:
    name = AppCloudDiskName
    flag = 'cd'
    type_flag = u'default'
    is_show = False
    desc = u'存储文件,统一校验文件权限'
    role_list = []


used_app = [AppCloudDisk]
