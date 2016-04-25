#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/24 下午4:09
# file: im_tools.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyuim.models import Friend, TalkUser
from util.jsonresult import get_result


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

