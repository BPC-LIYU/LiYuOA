#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/24 下午4:09
# file: im_tools.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyuim import IM_GROUPS_AND_MEMBERS
from liyuim.models import Friend, TalkUser
from liyuim.rpc.im_commend import mqtt_commend
from util.jsonresult import get_result
from django.core.cache import cache


def check_friend_relation(friend_id_parm_name='friend_id'):
    """
    检测friend_id 是否和用户具有好友关系,并将friend对象传递给参数
    by:王健 at:2016-04-24
    :param friend_id_parm_name:friend_id 在参数中的 key值
    :return:
    """

    def check_friend_relation_func(func=None):
        def test(request, *args, **kwargs):
            friend_id = kwargs[friend_id_parm_name]
            try:
                friend = Friend.objects.get(friend_id=friend_id, owner=request.user, is_active=True)
                kwargs['friend'] = friend
                return func(request, *args, **kwargs)
            except Friend.DoesNotExist:
                return get_result(False, u'该用户不是您的好友')

        return test

    return check_friend_relation_func


def check_group_relation(group_id_parm_name='talkgroup_id'):
    """
    talkgroup_id 是否和用户具有好友关系,并将friend对象传递给参数
    by:王健 at:2016-04-24
    :param group_id_parm_name:talkgroup_id 在参数中的 key值
    :return:
    """

    def check_group_relation_func(func=None):
        def test(request, *args, **kwargs):
            talkgroup_id = kwargs[group_id_parm_name]
            try:
                talkuser = TalkUser.objects.get(talkgroup_id=talkgroup_id, user=request.user, is_active=True)
                kwargs['talkuser'] = talkuser
                return func(request, *args, **kwargs)
            except Friend.DoesNotExist:
                return get_result(False, u'您不是该群的成员')

        return test

    return check_group_relation_func

#
# def clean_talk_groups_cache(group_id):
#     """
#     清空缓存中的组织结构
#     :param org_id:
#     :return:
#     """
#     cache_key = IM_GROUPS_AND_MEMBERS % group_id
#     cache.delete(cache_key)
#
#
# def get_talk_group_cache(group_id):
#     """
#     获取组织结构的缓存
#     by:王健 at:2016-04-29
#     :param group_id:
#     :return:
#     """
#     cache_key = IM_GROUPS_AND_MEMBERS % group_id
#
#     result = cache.get(cache_key)
#     if result is None:
#         result = {}
#         for person in TalkUser.objects.list_json().filter(talkgroup=group_id, is_active=True):
#             result[person['user_id']] = person
#
#         cache.set(cache_key, result)
#     return result
#
#
# def get_talk_member_ids_by_role(group_id, role=[0, 1]):
#     """
#     获取组织的管理员id列表
#     by:王健 at:2016-04-30
#     :param org_id:
#     :return:
#     """
#     result = get_talk_group_cache(group_id)
#     user_ids = []
#
#     for k, p in result.items():
#         if p['role'] in role:
#             user_ids.append(k)
#     return user_ids


def im_commend(event, group_id, parms={}):
    """
    分组事件:
    :param parms:
    :param group_id:
    :param event:
    :return:
    """
    # if user_ids is None:
    #     user_ids = get_talk_member_ids_by_role(group_id)

    mqtt_commend("imgroup", {"event_type": event, "event_obj": { "group_id": group_id, "parms": parms}})


def im_friend_commend(event, owner_id, friend_id, parms={}):
    """
    好友事件:
    :param parms:
    :param friend_id:
    :param owner_id:
    :param event:
    :return:
    """
    # if user_ids is None:
    #     user_ids = get_talk_member_ids_by_role(group_id)

    mqtt_commend("imfriend", {"event_type": event, "event_obj": { "owner_id": owner_id, "friend_id": friend_id, "parms": parms}})
