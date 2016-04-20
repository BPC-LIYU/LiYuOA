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
    role_desc = u'获取组织中的组织架构,查询成员信息'


class SySLeader:
    role = 'leader'
    role_name = u'主管'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppSysName, role_name)
    role_desc = u'新增、修改部门和部门内的成员'


class SySManager:
    role = 'manager'
    role_name = u'应用管理员'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppSysName, role_name)
    role_desc = u'新增、修改、删除所有部门和部门内的成员,设置部门的主管和助手,设置用户和应用的权限,设置新的应用管理员'


class AppSys:
    name = AppSysName
    flag = 'sys'
    type_flag = u'default'
    is_show = False
    desc = u'组织中的组织架构,涉及分组、权限、用户管理等功能'
    role_list = [SySUser, SySLeader, SySManager]

    User = SySUser
    Leader = SySLeader
    Manager = SySManager

AppDevelopName = u'开发者应用'


class User:
    role = 'user'
    role_name = u'用户'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppDevelopName, role_name)
    role_desc = u'获取组织中的组织架构,查询成员信息'


class Leader:
    role = 'leader'
    role_name = u'主管'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppDevelopName, role_name)
    role_desc = u'新增、修改部门和部门内的成员'


class Manager:
    role = 'manager'
    role_name = u'应用管理员'
    role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppDevelopName, role_name)
    role_desc = u'新增、修改、删除所有部门和部门内的成员,设置部门的主管和助手,设置用户和应用的权限,设置新的应用管理员'


class AppDevelop:
    name = AppDevelopName
    flag = 'develop'
    type_flag = u'default'
    is_show = False
    desc = u'组织中的组织架构,涉及分组、权限、用户管理等功能'
    role_list = [User, Leader, Manager]

    User = User
    Leader = Leader
    Manager = Manager

used_app = [AppDevelop]
