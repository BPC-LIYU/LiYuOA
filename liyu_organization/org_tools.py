#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/27 上午8:48
# file: org_tools.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyu_organization.models import Person, Group
from util.jsonresult import get_result


def check_org_relation(org_id_parm_name='org_id'):
    """
    检测org_id 是否和用户具有组织关系,并将person对象传递给参数
    by:王健 at:2016-04-24
    :param org_id_parm_name:org_id 在参数中的 key值
    :return:
    """

    def check_org_relation_func(func=None):
        def test(request, *args, **kwargs):
            org_id = kwargs[org_id_parm_name]
            try:
                person = Person.objects.get(org_id=org_id, user=request.user, is_active=True)
                kwargs['person'] = person
                return func(request, *args, **kwargs)
            except Person.DoesNotExist:
                return get_result(False, u'您不是该组织成员')

        return test

    return check_org_relation_func


def check_org_manager_relation(org_id_parm_name='org_id'):
    """
    检测org_id 是否和用户具有组织关系,并将person对象传递给参数
    by:王健 at:2016-04-24
    :param org_id_parm_name:org_id 在参数中的 key值
    :return:
    """

    def check_org_manager_relation_func(func=None):
        def test(request, *args, **kwargs):
            org_id = kwargs[org_id_parm_name]
            try:
                person = Person.objects.get(org_id=org_id, user=request.user, is_active=True)
                kwargs['person'] = person
                if person.manage_type not in [1, 2]:
                    return get_result(False, u'您不是该组织管理员')
                return func(request, *args, **kwargs)
            except Person.DoesNotExist:
                return get_result(False, u'您不是该组织成员')

        return test

    return check_org_manager_relation_func


def check_group(org_id_parm_name='org_id', group_id_parm_name='group_id'):
    """
    检测org_id 是否和用户具有组织关系,并将person对象传递给参数
    by:王健 at:2016-04-24
    :param org_id_parm_name:org_id 在参数中的 key值
    :param group_id_parm_name:group_id 在参数中的 key值
    :return:
    """

    def check_org_relation_func(func=None):
        def test(request, *args, **kwargs):
            org_id = kwargs[org_id_parm_name]
            group_id = kwargs[group_id_parm_name]
            try:
                group = Group.objects.get(group_id=group_id, org_id=org_id, is_active=True)
                kwargs['group'] = group
                return func(request, *args, **kwargs)
            except Person.DoesNotExist:
                return get_result(False, u'分组不存在,无法操作')

        return test

    return check_org_relation_func
