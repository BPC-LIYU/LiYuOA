#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午7:27
# file:app_config.py
# Email: wangjian2254@icloud.com
# Author: 王健

# APP_NAMESPACE = 'liyu_organization'

AppIMName = u'即时通信'


class User:
    role = 'user'
    role_name = u'用户'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppIMName, role_name)
    role_desc = u'即时通信用户'


class Leader:
    role = 'leader'
    role_name = u'主管'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppIMName, role_name)
    role_desc = u'即时通信管理用户'


class Manager:
    role = 'manager'
    role_name = u'应用管理员'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppIMName, role_name)
    role_desc = u'即时通信管理主管'


class AppIM:
    name = AppIMName
    flag = 'chat'
    type_flag = u'default'
    is_show = False
    desc = u'即时通信应用'
    role_list = [User, Leader, Manager]

    User = User
    Leader = Leader
    Manager = Manager


used_app = [AppIM]
