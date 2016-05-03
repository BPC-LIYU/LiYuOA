#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/23 上午11:48
# file: views_friend.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyuim.im_tools import check_friend_relation, im_friend_commend
from liyuim.models import Friend, FriendApply
from util.jsonresult import get_result
from util.loginrequired import client_login_required, check_request_parmes


@check_request_parmes(page_index=("页码", "int", 1), page_size=("页长度", "int", 50))
@client_login_required
def query_my_friend_list(request, page_index, page_size):
    """
    查询我的好友列表,分页
    :param request:
    :param page_index:
    :param page_size:
    :return:
    查询我的所有好友,分页
    """
    query = Friend.objects.list_json().filter(owner=request.user).filter(is_active=True, is_black=False)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(page_index=("页码", "int", 1), page_size=("页长度", "int", 50))
@client_login_required
def query_friendapply_list(request, page_index, page_size):
    """
    查询好友申请,分页
    :param request:
    :param page_index:
    :param page_size:
    :return:
    """
    query = FriendApply.objects.list_json().filter(friend=request.user).filter(is_active=True).order_by('-create_time')
    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(user_id=("申请的好友用户id", "r,int"), content=("申请内容", "r"))
@client_login_required
def apply_friend(request, user_id, content):
    """
    申请添加好友
    :param request:
    :param user_id:
    :return:
    申请添加好友
    by:王健 at:2016-04-24
    增加好友变动的事件
    by:王健 at:2016-05-03
    """
    friend_apply = FriendApply()
    friend_apply.friend_id = user_id
    friend_apply.content = content
    friend_apply.owner = request.user
    friend_apply.save()
    im_friend_commend("apply_friend", request.user.id, user_id, friend_apply.toJSON())
    return get_result(True, None, friend_apply)


@check_request_parmes(friendapply_id=("好友申请id", "r,int"))
@client_login_required
def pass_friendapply(request, friendapply_id):
    """
    修改好友申请
    :param request:
    :param friendapply_id:
    :return:
    修改好友申请
    by:王健 at:2016-04-24
    增加好友变动的事件
    by:王健 at:2016-05-03
    """
    try:
        friendapply = FriendApply.objects.get(id=friendapply_id, owner=request.user, is_active=True)
        friendapply.copy_old()
        friendapply.status = 1
        created, diff = friendapply.compare_old()
        if diff:
            friend, created = Friend.objects.get_or_create(friend=friendapply.friend, owner=request.user)
            if not created:
                friend.is_active = True
            friend.save()
            friend, created = Friend.objects.get_or_create(owner=friendapply.friend, friend=request.user)
            if not created:
                friend.is_active = True
            friend.save()
            im_friend_commend("pass_friendapply", friendapply.owner_id, friendapply.friend_id, friendapply.toJSON())
            return get_result(True, u'好友申请处理成功', friendapply)
        else:
            return get_result(False, u'已经处理过的申请,不能再次处理', friendapply)
    except FriendApply.DoesNotExist:
        return get_result(False, u'好友申请,不是发给您的,您无权处理')


@check_request_parmes(friend_id=("好友id", "r,int"))
@client_login_required
def add_friend(request, friend_id):
    """
    直接添加好友
    :param request:
    :param friend_id:
    :return:
    直接添加好友
    by:王健 at:2016-04-24
    增加好友变动的事件
    by:王健 at:2016-05-03
    """
    friend, created = Friend.objects.get_or_create(friend_id=friend_id, owner=request.user)
    if not created:
        friend.is_active = True
    friend.save()
    im_friend_commend("add_friend", friend.owner_id, friend.friend_id, friend.toJSON())
    return get_result(True, u'添加好友成功')


@check_request_parmes(friendapply_id=("好友申请id", "r,int"))
@client_login_required
def reject_friendapply(request, friendapply_id):
    """
    拒绝好友申请(删除)
    :param request:
    :param friendapply_id:
    :return:
    拒绝好友申请(删除)
    by:王健 at:2016-04-24
    增加好友变动的事件
    by:王健 at:2016-05-03
    """
    try:
        friendapply = FriendApply.objects.get(id=friendapply_id, owner=request.user, is_active=True)
        friendapply.copy_old()
        friendapply.is_active = False
        friendapply.compare_old()
        friendapply.save()
        im_friend_commend("reject_friendapply", friendapply.owner_id, friendapply.friend_id, friendapply.toJSON())
        return get_result(True, u'好友申请删除成功', friendapply)
    except FriendApply.DoesNotExist:
        return get_result(False, u'好友申请,不是发给您的,您无权处理')


@check_request_parmes(friend_id=("好友id", "r,int"), nickname=("昵称", ""))
@client_login_required
@check_friend_relation()
def modefy_friend_nickname(request, friend_id, nickname, friend):
    """
    修改好友备注名称
    :param request:
    :param friend_id:
    :return:
    修改好友备注名称
    by:王健 at:2016-04-24
    增加好友变动的事件
    by:王健 at:2016-05-03
    """
    friend.copy_old()
    friend.nickname = nickname
    friend.compare_old()
    friend.save()
    im_friend_commend("friend_change", friend.owner_id, friend.friend_id, friend.toJSON())
    return get_result(True, u'修改好友昵称成功', friend)


@check_request_parmes(friend_id=("好友id", "r,int"), is_black=("是否黑名单", "r,b"))
@client_login_required
@check_friend_relation()
def mark_friend_black(request, friend_id, is_black, friend):
    """
    设置好友到黑名单
    :param friend: check_friend_relation 装饰器 注入的 friend对象
    :param is_black:
    :param request:
    :param friend_id:
    :return:
    设置好友到黑名单
    by:王健 at:2016-04-24
    增加好友变动的事件
    by:王健 at:2016-05-03
    """
    friend.copy_old()
    friend.is_black = is_black
    friend.compare_old()
    friend.save()
    im_friend_commend("friend_change", friend.owner_id, friend.friend_id, friend.toJSON())
    return get_result(True, u'修改好友昵称成功', friend)


@check_request_parmes(friend_id=("好友id", "r,int"), is_muted=("是否免扰", "r,b"))
@client_login_required
@check_friend_relation()
def mark_friend_muted(request, friend_id, is_muted, friend):
    """
    设置好友免扰
    :param friend: check_friend_relation 装饰器 注入的 friend对象
    :param is_muted:
    :param request:
    :param friend_id:
    :return:
    设置好友免扰
    by:王健 at:2016-04-24
    增加好友变动的事件
    by:王健 at:2016-05-03
    """
    friend.copy_old()
    friend.is_muted = is_muted
    friend.compare_old()
    im_friend_commend("friend_change", friend.owner_id, friend.friend_id, friend.toJSON())
    return get_result(True, u'修改好友昵称成功', friend)


@check_request_parmes(page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
def query_black_friend_list(request, page_index, page_size):
    """
    查询黑名单列表
    :param page_size:
    :param page_index:
    :param :
    :param request:
    :return:
    查询黑名单列表
    by:王健 at:2016-04-24
    """
    query = Friend.objects.list_json().filter(owner=request.user, is_active=True).filter(is_black=True)

    return get_result(True, None, query.get_page(page_index, page_size))


