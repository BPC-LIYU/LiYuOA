#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/24 上午9:20
# file: views_talkgroup.py
# Email: wangjian2254@icloud.com
# Author: 王健
import hashlib
import time

from liyuim.im_tools import check_group_relation
from liyuim.models import TalkGroup, TalkUser, TalkApply
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required


@check_request_parmes(page_index=("页码", "int", 1), page_size=("页长度", "int", 50))
@client_login_required
def query_my_talkgroup_list(request, page_index, page_size):
    """
    查询我的群组列表,分页
    :param request:
    :param page_index:
    :param page_size:
    :return:
    查询我的所有群组,分页
    """
    query = TalkGroup.objects.list_json().filter(talkuser__user=request.user).filter(is_active=True)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(flag=("群成员md5", "r"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
def query_group_by_flag_list(request, flag, page_index, page_size):
    """
    查询群组,根据成员md5值列表
    :param page_size:
    :param page_index:
    :param flag:
    :param request:
    :return:
    查询群组,根据成员md5值列表
    by:王健 at:2016-04-24
    """
    query = TalkGroup.objects.list_json().filter(is_active=True, flag=flag).filter(talkuser=request.user)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(name=("群名称", "r"), group_type=("群类型", "r,int"), member_ids=("成员id列表", "r,[int]"))
@client_login_required
def create_talkgroup(request, name, group_type, member_ids):
    """
    创建群
    :param member_ids:
    :param group_type:
    :param request:
    :param name:
    :return:
    创建群
    by:王健 at:2016-04-24
    """
    member_ids.sort()
    flag = hashlib.md5(','.join(member_ids)).hexdigest()
    talkgroup = TalkGroup()
    talkgroup.name = name
    talkgroup.group_type = group_type
    talkgroup.flag = flag
    talkgroup.owner = request.user
    talkgroup.save()

    for uid in member_ids:
        talkuser = TalkUser()
        talkuser.talkgroup = talkgroup
        talkuser.user_id = uid
        talkuser.role = 0
        talkuser.read_timeline = int(time.time())
        talkuser.save()

    return get_result(True, u'创建群成功', talkgroup)


@check_request_parmes(talkgroup_id=("群id", "r,int"))
@client_login_required
@check_group_relation
def get_talkgroup(request, talkgroup_id, talkuser):
    """
    查询群信息信息
    :param talkuser:
    :param talkgroup_id:
    :param request:
    :return:
    查询群信息信息
    by:王健 at:2016-04-24
    """
    obj = talkuser.talk
    num = TalkUser.objects.filter(talk=talkgroup_id, is_active=True).count()
    obj.extend(num=num)
    return get_result(True, None, obj)


@check_request_parmes(talkgroup_id=("群id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
@check_group_relation
def query_talkgroup_member_list(request, talkgroup_id, talkuser, page_index, page_size):
    """
    查询群成员列表列表
    :param page_size:
    :param page_index:
    :param talkgroup_id:
    :param request:
    :return:
    查询群成员列表列表
    by:王健 at:2016-04-24
    """
    query = TalkUser.objects.list_json().filter(is_active=True, talkgroup=talkuser.talkgroup)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(talkgroup_id=("群id", "r,int"))
@client_login_required
@check_group_relation
def quite_talkgroup(request, talkgroup_id, talkuser):
    """
    退出群
    :param request:
    :param talkgroup_id:
    :return:
    退出群
    by:王健 at:2016-04-25
    """
    if talkuser.talkgroup.owner_id == request.user.id:
        return get_result(False, u'群主不能退出群')
    talkuser.copy_old()
    talkuser.is_active = False
    talkuser.compare_old()
    talkuser.save()
    return get_result(True, u'退出群成功')


@check_request_parmes(talkgroup_id=("群id", "r,int"))
@client_login_required
@check_group_relation
def dismiss_talkgroup(request, talkgroup_id, talkuser):
    """
    解散群
    :param request:
    :param talkgroup_id:
    :return:
    解散群
    by:王健 at:2016-04-25
    """
    if talkuser.talkgroup.owner_id != request.user.id:
        return get_result(False, u'只有群主能解散群')
    talkgroup = talkuser.talkgroup
    talkgroup.copy_old()
    talkgroup.is_active = False
    talkgroup.compare_old()
    talkgroup.save()
    TalkUser.objects.filter(talkgroup_id=talkgroup_id, is_active=True).update(is_active=False)
    return get_result(True, u'退出群成功')


@check_request_parmes(talkgroup_id=("群id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_group_relation
def remove_talkgroup(request, talkgroup_id, user_id, talkuser):
    """
    踢出群
    :param talkuser:
    :param user_id:
    :param request:
    :param talkgroup_id:
    :return:
    踢出群
    by:王健 at:2016-04-25
    """
    if talkuser.talkgroup.owner_id != request.user.id and talkuser.role != 1:
        return get_result(False, u'只有群主和管理员才能踢人出群')
    member = TalkUser.objects.get(talkgroup_id=talkgroup_id, user_id=user_id)
    member.copy_old()
    member.is_active = False
    member.compare_old()
    member.save()
    return get_result(True, u'踢出群成功')


@check_request_parmes(talkgroup_id=("群id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_group_relation
def add_talkgroup(request, talkgroup_id, user_id, talkuser):
    """
    拉人入群
    :param talkuser:
    :param user_id:
    :param request:
    :param talkgroup_id:
    :return:
    拉人入群
    by:王健 at:2016-04-25
    """
    if not talkuser.talkgroup.is_add and talkuser.talkgroup.owner_id != request.user.id and talkuser.role != 1:
        return get_result(False, u'只有群主和管理员才能拉人入群')

    member, created = TalkUser.objects.get_or_create(talkgroup_id=talkgroup_id, user_id=user_id)
    member.copy_old()
    member.is_active = True
    member.read_timeline = int(time.time())
    member.is_muted = False
    member.compare_old()
    member.save()
    return get_result(True, u'踢出群成功')


@check_request_parmes(talkgroup_id=("群id", "r,int"), content=("用户内容", "r"))
@client_login_required
def apply_talkgroup(request, talkgroup_id, content):
    """
    拉人入群
    :param content:
    :param request:
    :param talkgroup_id:
    :return:
    拉人入群
    by:王健 at:2016-04-25
    """

    talkapply = TalkApply()
    talkapply.owner = request.user
    talkapply.talkgroup_id = talkgroup_id
    talkapply.status = 0
    talkapply.content = content
    talkapply.save()

    return get_result(True, u'发出入群申请成功', talkapply)


@check_request_parmes(talkapply_id=("入群申请id", "r,int"))
@client_login_required
def pass_talkapply(request, talkapply_id):
    """
    通过入群申请
    :param talkapply_id:
    :param request:
    :return:
    拉人入群
    by:王健 at:2016-04-25
    """
    try:
        talkapply = TalkApply.objects.get(pk=talkapply_id)
        if talkapply.talkgroup.owner_id == request.user.id or TalkUser.objects.filter(user=request.user, is_active=True,
                                                                                      role=1).exists():
            talkapply.status = 1
            talkapply.checker = request.user
            talkapply.save()
        else:
            return get_result(False, u'只有群主和管理员才能操作入群申请')
    except TalkApply.DoesNotExist:
        return get_result(False, u'找不到这条入群申请')


@check_request_parmes(talkapply_id=("入群申请id", "r,int"), reply=("拒绝理由", ""))
@client_login_required
def reject_talkapply(request, talkapply_id, reply):
    """
    通过入群申请
    :param reply:
    :param talkapply_id:
    :param request:
    :return:
    拉人入群
    by:王健 at:2016-04-25
    """
    try:
        talkapply = TalkApply.objects.get(pk=talkapply_id)
        if talkapply.talkgroup.owner_id == request.user.id or TalkUser.objects.filter(user=request.user, is_active=True,
                                                                                      role=1).exists():
            talkapply.status = 2
            talkapply.checker = request.user
            talkapply.reply = reply
            talkapply.save()
        else:
            return get_result(False, u'只有群主和管理员才能操作入群申请')
    except TalkApply.DoesNotExist:
        return get_result(False, u'找不到这条入群申请')


@check_request_parmes(talkgroup_id=("群id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_group_relation
def add_talkgroup_manager(request, talkgroup_id, user_id, talkuser):
    """
    添加管理员
    :param talkuser:
    :param user_id:
    :param request:
    :param talkgroup_id:
    :return:
    添加管理员
    by:王健 at:2016-04-25
    """
    if talkuser.talkgroup.owner_id != request.user.id:
        return get_result(False, u'只有群主才能添加管理员')
    try:
        member = TalkUser.objects.get(talkgroup_id=talkgroup_id, user_id=user_id, is_active=True)
        member.copy_old()
        member.role = 1
        member.compare_old()
        member.save()
        return get_result(True, u'添加管理员成功')
    except TalkUser.DoesNotExist:
        return get_result(False, u'只有成员才能被设置成管理员身份')


@check_request_parmes(talkgroup_id=("群id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_group_relation
def remove_talkgroup_manager(request, talkgroup_id, user_id, talkuser):
    """
    拉人入群
    :param talkuser:
    :param user_id:
    :param request:
    :param talkgroup_id:
    :return:
    拉人入群
    by:王健 at:2016-04-25
    """
    if talkuser.talkgroup.owner_id != request.user.id:
        return get_result(False, u'只有群主才能删除管理员')
    try:
        member = TalkUser.objects.get(talkgroup_id=talkgroup_id, user_id=user_id, is_active=True)
        member.copy_old()
        member.role = 0
        member.compare_old()
        member.save()
        return get_result(True, u'删除管理员成功')
    except TalkUser.DoesNotExist:
        return get_result(False, u'只有成员才能被取消管理员身份')


@check_request_parmes(talkgroup_id=("群id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_group_relation
def transfer_talkgroup_manager(request, talkgroup_id, user_id, talkuser):
    """
    转让群
    :param talkuser:
    :param user_id:
    :param request:
    :param talkgroup_id:
    :return:
    拉人入群
    by:王健 at:2016-04-25
    """
    if talkuser.talkgroup.owner_id != request.user.id:
        return get_result(False, u'只有群主才能转让群')
    try:
        member = TalkUser.objects.get(talkgroup_id=talkgroup_id, user_id=user_id, is_active=True)
        talkgroup = talkuser.talkgroup
        talkgroup.copy_old()
        talkgroup.owner = member
        talkgroup.compare_old()
        talkgroup.save()
        return get_result(True, u'转让群成功')
    except TalkUser.DoesNotExist:
        return get_result(False, u'只有群主才能转让群')


@check_request_parmes(talkgroup_id=("群id", "r,int"), user_id=("用户id", "r,int"), nickname=("昵称", "r"))
@client_login_required
@check_group_relation
def update_nick_in_talkgroup(request, talkgroup_id, user_id, nickname, talkuser):
    """
    转让群
    :param talkuser:
    :param user_id:
    :param request:
    :param talkgroup_id:
    :return:
    拉人入群
    by:王健 at:2016-04-25
    """
    if talkuser.talkgroup.owner_id != request.user.id and talkuser.role != 1:
        return get_result(False, u'只有群主和管理员才能修改别人的昵称')
    try:
        member = TalkUser.objects.get(talkgroup_id=talkgroup_id, user_id=user_id, is_active=True)
        member.copy_old()
        member.nickname = nickname
        member.compare_old()
        member.save()
        return get_result(True, u'修改昵称成功')
    except TalkUser.DoesNotExist:
        return get_result(False, u'该用户不是群成员')


@check_request_parmes(talkgroup_id=("群id", "r,int"), nickname=("昵称", "r"), is_muted=("是否免打扰", "b"))
@client_login_required
@check_group_relation
def update_info_in_talkgroup(request, talkgroup_id, is_muted, nickname, talkuser):
    """
    修改自己的群属性
    :param talkuser:
    :param user_id:
    :param request:
    :param talkgroup_id:
    :return:
    修改自己的群属性
    by:王健 at:2016-04-25
    """
    talkuser.copy_old()
    talkuser.nickname = nickname
    talkuser.is_muted = is_muted
    talkuser.compare_old()
    talkuser.save()
    return get_result(True, u'修改群属性成功')



# todo:\设置我的群属性(昵称\免扰)
