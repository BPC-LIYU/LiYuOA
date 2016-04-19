#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午7:27
# file:app_config.py
# Email: wangjian2254@icloud.com
# Author: 王健

APP_NAMESPACE = 'liyu_organization'


class AppOrganization:
    namespace = APP_NAMESPACE
    name = u'组织架构'
    flag = 'organization'
    type_flag = u'default'
    is_show = False
    desc = u'组织中的组织架构,涉及分组、权限、用户管理等功能'

    class User:
        role = 'user'
        role_name = u'用户'
        role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppOrganization.name, role_name)
        role_desc = u'获取组织中的组织架构,查询成员信息'

    class Leader:
        role = 'leader'
        role_name = u'主管'
        role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppOrganization.name, role_name)
        role_desc = u'新增、修改部门和部门内的成员'

    class Manager:
        role = 'manager'
        role_name = u'应用管理员'
        role_message = u'权限不足,您需要联系管理员,将您的账号在%s 应用中设置为:%s 角色' % (AppOrganization.name, role_name)
        role_desc = u'新增、修改、删除所有部门和部门内的成员,设置部门的主管和助手,设置用户和应用的权限,设置新的应用管理员'

    role_list = [User, Leader, Manager]


used_app = [AppOrganization]
