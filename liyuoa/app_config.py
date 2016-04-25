#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午7:27
# file:app_config.py
# Email: wangjian2254@icloud.com
# Author: 王健

# APP_NAMESPACE = 'liyu_organization'


AppSysName = u'系统基础'


class SySUser:
    role = 'user'
    role_name = u'用户'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppSysName, role_name)
    role_desc = u'系统用户'


class SySLeader:
    role = 'leader'
    role_name = u'主管'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppSysName, role_name)
    role_desc = u'系统主管,创建、查询、管理组织'


class SySManager:
    role = 'manager'
    role_name = u'应用管理员'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppSysName, role_name)
    role_desc = u'管理系统主管'


class AppSys:
    name = AppSysName
    flag = 'sys'
    type_flag = u'default'
    is_show = False
    desc = u'系统中用户、组织、应用管理'
    role_list = [SySUser, SySLeader, SySManager]

    User = SySUser
    Leader = SySLeader
    Manager = SySManager

AppDevelopName = u'开发者应用'


class User:
    role = 'user'
    role_name = u'用户'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppDevelopName, role_name)
    role_desc = u'开发人员'


class Leader:
    role = 'leader'
    role_name = u'主管'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppDevelopName, role_name)
    role_desc = u'开发人员设置接口和开发者信息'


class Manager:
    role = 'manager'
    role_name = u'应用管理员'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppDevelopName, role_name)
    role_desc = u'管理开发主管'


class AppDevelop:
    name = AppDevelopName
    flag = 'develop'
    type_flag = u'default'
    is_show = False
    desc = u'开发项目的相关工具'
    role_list = [User, Leader, Manager]

    User = User
    Leader = Leader
    Manager = Manager

used_app = [AppSys, AppDevelop]
