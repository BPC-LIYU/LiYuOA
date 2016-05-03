#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/27 上午8:48
# file: org_tools.py
# Email: wangjian2254@icloud.com
# Author: 王健
from django.core.cache import cache

from liyu_organization import ORGANIZATION_GROUPS_AND_MEMBERS
from liyu_organization.models import Person, Group
from liyuim.rpc.im_commend import mqtt_commend
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


def check_person_group_permiss(person, group, h_level=False):
    """
    检查成员在分组的权限
    :param person:
    :param group:
    :return:
    """
    if person.manage_type in [1, 2]:
        return True
    if group.parent_id is None:
        if group.charge_id is not None:
            if group.charge_id == person.id:
                return True
        if not h_level and group.aide_id is not None:
            if group.aide_id == person.id:
                return True
    else:
        if group.parent.charge_id is not None:
            if group.parent.charge_id == person.id:
                return True
        if group.parent.aide_id is not None:
            if group.parent.aide_id == person.id:
                return True
    return False





def clean_organization_groups_cache(org_id):
    """
    清空缓存中的组织结构
    :param org_id:
    :return:
    """
    cache_key = ORGANIZATION_GROUPS_AND_MEMBERS % org_id
    cache.delete(cache_key)


def get_organization_cache(org_id):
    """
    获取组织结构的缓存
    by:王健 at:2016-04-29
    :param org_id:
    :return:
    """
    cache_key = ORGANIZATION_GROUPS_AND_MEMBERS % org_id

    result = cache.get(cache_key)
    if result is None:
        member_dict = {}
        group_dict = {}
        group_list = []
        weifenzu = []
        result = {'grouplist': group_list, 'weifenzu': weifenzu, 'person': member_dict, 'group': group_dict}
        group_member_ids = set()
        for person in Person.objects.list_json().filter(org_id=org_id, is_active=True):
            member_dict[person['user_id']] = person
        for group in Group.objects.filter(org_id=org_id, is_active=True).prefetch_related('members'):
            group_dict[group.id] = group.toJSON()
            group_dict[group.id]['member_ids'] = []
            group_dict[group.id]['grouplist'] = []
            if group.parent_id is None:
                group_list.append(group.id)
            for p in group.members.filter(is_active=True).values('user_id'):
                group_dict[group.id]['member_ids'].append(p['user_id'])
                group_member_ids.add(p['user_id'])

        weifenzu.extend(list(set(member_dict.keys()) - group_member_ids))
        for gid, group in group_dict.items():
            if group['parent_id']:
                group_dict[group['parent_id']]['grouplist'].append(gid)

        cache.set(cache_key, result)
    return result


def get_organization_groups(org_id, group_id=None):
    """
    查询组织结构, 计算各组人员
    :param group_id:
    :param org_id:
    :return:
    """

    result = get_organization_cache(org_id)
    obj = {'members': [], 'groups': [], 'name': None, 'id': None, 'group_link': []}
    if group_id is None:
        for uid in result['weifenzu']:
            obj['members'].append(result['person'][uid])

        for gid in result['grouplist']:
            obj['groups'].append(result['group'][gid])

    else:
        group = result['group'][int(group_id)]
        obj['name'] = group['name']
        obj['id'] = group['id']
        for uid in group['member_ids']:
            obj['members'].append(result['person'][uid])

        for gid in group['grouplist']:
            obj['groups'].append(result['group'][gid])

        # 计算出分组父级链
        link = []
        obj['group_link'] = link
        i = 0
        tmp_group = group
        while tmp_group is not None:
            link.append(tmp_group)
            if tmp_group['parent_id']:
                tmp_group = result['group'][tmp_group['parent_id']]
            else:
                tmp_group = None
            i += 1
            if i > 100:
                tmp_group = None

    return obj


def get_org_member_ids_by_manage_type(org_id, manage_type=[0, 1, 2]):
    """
    获取组织的管理员id列表
    by:王健 at:2016-04-30
    :param org_id:
    :return:
    """
    result = get_organization_cache(org_id)
    user_ids = []

    for k, p in result['person'].items():
        if p['manage_type'] in manage_type:
            user_ids.append(k)
    return user_ids


def org_commend(event, org_id, message, user_ids=None):
    """
    组织事件:
    :param event:
    :param org_id:
    :param message:
    :return:
    """
    if user_ids is None:
        user_ids = get_org_member_ids_by_manage_type(org_id)

    mqtt_commend("org", {"event_type": event, "event_obj": {"org_id": org_id, "message": message, "user_ids": user_ids}})
