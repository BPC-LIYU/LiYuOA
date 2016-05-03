#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/27 上午10:16
# file: views_group.py
# Email: wangjian2254@icloud.com
# Author: 王健
import hashlib

from liyu_organization.models import Group, Person
from liyu_organization.org_tools import check_org_relation, check_group, get_organization_groups, \
    clean_organization_groups_cache, org_commend, check_person_group_permiss
from liyuim.im_tools import im_commend
from liyuim.models import TalkGroup, TalkUser
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required


@check_request_parmes(org_id=("组织id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation()
def query_group_by_org_list(request, org_id, page_index, page_size, person):
    """
    查询组织中的部门列表,顶级部门
    :param person:
    :param page_size:
    :param page_index:
    :param org_id:
    :param request:
    :return:
    查询组织中的部门列表
    by:王健 at:2016-04-27
    """
    query = Group.objects.list_json().filter(is_active=True)

    query = query.filter(org_id=org_id, parent=None)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"), page_index=("页码", "int", 1),
                      page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation()
def query_group_by_group_list(request, org_id, group_id, page_index, page_size, person):
    """
    查询组织中的部门列表,顶级部门
    :param group_id:
    :param person:
    :param page_size:
    :param page_index:
    :param org_id:
    :param request:
    :return:
    查询组织中的部门列表
    by:王健 at:2016-04-27
    """
    query = Group.objects.list_json().filter(is_active=True)

    query = query.filter(org_id=org_id, parent_id=group_id)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(page_index=("页码", "int", 1), page_size=("页长度", "int", 200))
@client_login_required
def query_group_by_my_list(request, page_index, page_size):
    """
    查询组织中的部门列表,顶级部门
    :param page_size:
    :param page_index:
    :param request:
    :return:
    查询组织中的部门列表
    by:王健 at:2016-04-27
    """
    query = Group.objects.list_json().filter(is_active=True)

    query = query.filter(members=request.user.id)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "int"), name=("部门名称", ""),
                      charge_id=("主管id", "int"), aide_id=("主管id", "int"), is_create_talk_group=("是否创建部门群", "b", False))
@client_login_required
@check_org_relation()
def create_group(request, org_id, group_id, charge_id, aide_id, is_create_talk_group, name, person):
    """
    创建部门
    :param is_create_talk_group:
    :param request:
    :param org_id:
    :return:
    创建部门
    by:王健 at:2016-04-27
    创建部门时可以提供主管 和 主管助理的参数
    by:王健 at:2016-04-29
    部门变动事件
    by:王健 at:2016-05-03
    """
    group = None
    if group_id is None:
        if person.manage_type not in [1, 2]:
            return get_result(False, u'只有管理员才能创建一级部门')
    else:
        try:
            group = Group.objects.get(org_id=org_id, pk=group_id, is_active=True)
        except Group.DoesNotExist:
            return get_result(False, u'部门不存在,不能创建子部门')
        if person.manage_type not in [1,
                                      2] and group.charge.user_id != request.user_id and group.aide.user_id != request.user_id:
            return get_result(False, u'只有管理员、部门主管、部门主管助手 可以创建自部门')

    newgroup = Group()
    newgroup.org_id = org_id
    newgroup.name = name
    newgroup.parent = group
    if group is not None and (group.charge_id is not None or group.aide_id is not None):
        if (group.charge_id is not None and group.charge.user_id == request.user_id) or (group.aide_id is not None and group.aide.user_id == request.user_id):
            newgroup.charge_id = group.charge_id
            newgroup.aide_id = group.aide_id

    if charge_id:
        newgroup.charge_id = charge_id
    if aide_id:
        newgroup.aide_id = aide_id

    newgroup.save()
    if newgroup.charge_id:
        newgroup.members.add(newgroup.charge)
    if newgroup.aide_id:
        newgroup.members.add(newgroup.aide)

    if is_create_talk_group:
        imgroup = TalkGroup()
        imgroup.group_type = 2
        imgroup.name = newgroup.name
        if newgroup.charge_id:
            imgroup.owner_id = newgroup.charge.user_id
        if newgroup.aide_id and not imgroup.owner_id:
            imgroup.owner_id = newgroup.aide.user_id
        imgroup.save()

        member_ids = []
        if newgroup.charge_id:
            talkuser = TalkUser()
            talkuser.talkgroup = imgroup
            talkuser.user_id = newgroup.charge.user_id
            if imgroup.owner_id == talkuser.user_id:
                talkuser.role = 1
            talkuser.save()
            talkuser.push_im_event(request.user)
            member_ids.append(talkuser.user_id)
        if newgroup.aide_id:
            talkuser = TalkUser()
            talkuser.talkgroup = imgroup
            talkuser.user_id = newgroup.aide.user_id
            if imgroup.owner_id == talkuser.user_id:
                talkuser.role = 1
            talkuser.save()
            talkuser.push_im_event(request.user)
            member_ids.append(talkuser.user_id)

        if member_ids:
            imgroup.make_md5_flag()
            imgroup.save()
            im_commend("im_group_change", imgroup.id)

    org_commend("org_group_change", org_id, None)
    return get_result(True, u'创建部门成功', newgroup)


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"), name=("部门名称", ""),
                      icon_url=("头像", "url"), parent_id=("父级部门id", "int"))
@client_login_required
@check_org_relation()
@check_group()
def update_group(request, org_id, group_id, name, icon_url, parent_id, person, group):
    """
    修改部门的信息
    :param request:
    :param org_id:
    :return:
    修改部门的信息
    by:王健 at:2016-04-27
    部门变动事件
    by:王健 at:2016-05-03
    """
    if not check_person_group_permiss(person, group):
        return get_result(False, u'只有管理员、部门主管、部门主管助手、父级部门主管、父级部门主管助手可以修改部门信息')
    try:
        if parent_id is not None:
            parentgroup = Group.objects.get(org_id=org_id, pk=parent_id, is_active=True)
    except Group.DoesNotExist:
        return get_result(False, u'设置的父级部门不存在,无法修改')

    group.copy_old()
    if name:
        group.name = name
    if icon_url:
        group.icon_url = icon_url
    if parent_id:
        group.parent_id = parent_id
    created, diff = group.compare_old()

    if diff:
        group.save()
        org_commend("org_group_change", org_id, None)

    return get_result(True, u'修改部门信息成功', group)


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def remove_charge_group(request, org_id, person, group):
    """
    删除部门主管
    :param request:
    :param org_id:
    :return:
    删除部门主管
    by:王健 at:2016-04-27
    部门变动事件
    by:王健 at:2016-05-03
    """
    if check_person_group_permiss(person, group):
        group.copy_old()
        group.charge = None
        created, diff = group.compare_old()
        if diff:
            group.save()
            org_commend("org_group_change", org_id, None)
        return get_result(True, u'删除部门主管成功', group)
    else:
        return get_result(False, u'只有管理员、部门主管、部门主管助手、父级部门主管、父级部门主管助手可以修改部门信息')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def remove_aide_group(request, org_id, person, group):
    """
    删除部门主管
    :param request:
    :param org_id:
    :return:
    删除部门主管
    by:王健 at:2016-04-27
    部门变动事件
    by:王健 at:2016-05-03
    """
    if check_person_group_permiss(person, group):
        group.copy_old()
        group.aide = None
        created, diff = group.compare_old()
        if diff:
            group.save()
            org_commend("org_group_change", org_id, None)
        return get_result(True, u'删除部门主管助手成功', group)
    else:
        return get_result(False, u'只有管理员、部门主管、部门主管助手、父级部门主管、父级部门主管助手可以修改部门信息')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def add_charge_group(request, org_id, group_id, user_id, person, group):
    """
    添加部门主管
    :param request:
    :param org_id:
    :return:
    添加部门主管
    by:王健 at:2016-04-27
    部门变动事件
    by:王健 at:2016-05-03
    """
    if check_person_group_permiss(person, group, True):
        group.copy_old()
        try:
            group.charge = Person.objects.get(org_id=org_id, user_id=user_id, is_active=True)
        except Person.DoesNotExist:
            return get_result(False, u'用户不是当前组织的成员,不能设置成主管')
        created, diff = group.compare_old()
        if diff:
            group.save()
            org_commend("org_group_change", org_id, None)
            if group.talkgroup_id is not None:
                talkuser, created = TalkUser.objects.get_or_create(talkgroup_id=group.talkgroup_id, user_id=user_id)
                talkuser.copy_old()
                talkuser.is_active = True
                crea, diff = talkuser.compare_old()
                if created or diff:
                    talkuser.save()
                    talkuser.push_im_event(request.user)
                    im_commend("im_group_change", group.talkgroup_id)

        return get_result(True, u'设置部门主管成功', group)
    else:
        return get_result(False, u'只有管理员、部门主管、父级部门主管、父级部门主管助手可以添加部门主管')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def add_aide_group(request, org_id, user_id, person, group):
    """
    删除部门主管
    :param group:
    :param person:
    :param user_id:
    :param request:
    :param org_id:
    :return:
    删除部门主管
    by:王健 at:2016-04-27
    部门变动事件
    by:王健 at:2016-05-03
    """
    if check_person_group_permiss(person, group):

        group.copy_old()
        try:
            group.aide = Person.objects.get(org_id=org_id, user_id=user_id, is_active=True)
        except Person.DoesNotExist:
            return get_result(False, u'用户不是当前组织的成员,不能设置成主管助手')
        created, diff = group.compare_old()
        if diff:
            group.save()
            org_commend("org_group_change", org_id, None)
            if group.talkgroup_id is not None:
                talkuser, created = TalkUser.objects.get_or_create(talkgroup_id=group.talkgroup_id, user_id=user_id)
                talkuser.copy_old()
                talkuser.is_active = True
                crea, diff = talkuser.compare_old()
                if created or diff:
                    talkuser.save()
                    talkuser.push_im_event(request.user)
                    im_commend("im_group_change", group.talkgroup_id)

        return get_result(True, u'设置部门主管助手成功', group)
    else:
        return get_result(False, u'只有管理员、部门主管、部门主管助手、父级部门主管、父级部门主管助手可以添加部门主管助手')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def remove_group(request, org_id, person, group):
    """
    删除部门
    :param group:
    :param person:
    :param request:
    :param org_id:
    :return:
    删除部门
    by:王健 at:2016-04-27
    部门变动事件
    by:王健 at:2016-05-03
    """
    if check_person_group_permiss(person, group, True):

        if group.members.all().exist():
            return get_result(False, u'部门内还有成员, 请先移除成员')
        group.copy_old()
        group.is_active = False
        created, diff = group.compare_old()
        if diff:
            group.save()
            org_commend("org_group_change", org_id, None)
        return get_result(True, u'删除部门成功', group)
    else:
        return get_result(False, u'只有管理员、部门主管、父级部门主管、父级部门主管助手可以删除部门')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def add_person_group(request, org_id, user_id, person, group):
    """
    部门加人
    :param group:
    :param person:
    :param user_id:
    :param request:
    :param org_id:
    :return:
    部门加人
    by:王健 at:2016-04-27
    部门变动事件
    by:王健 at:2016-05-03
    """
    if check_person_group_permiss(person, group):

        try:
            group.members.add(Person.objects.get(org_id=org_id, user_id=user_id, is_active=True))

        except Person.DoesNotExist:
            return get_result(False, u'用户不是当前组织的成员,不能加入部门')
        clean_organization_groups_cache(org_id)
        org_commend("org_group_change", org_id, None)
        if group.talkgroup_id:
            talkuser, created = TalkUser.objects.get_or_create(talkgroup_id=group.talkgroup_id, user_id=user_id)
            talkuser.copy_old()
            talkuser.is_active = True
            crea, diff = talkuser.compare_old()
            if created or diff:
                talkuser.save()
                talkuser.push_im_event(request.user)
                im_commend("im_group_change", group.talkgroup_id)
        return get_result(True, u'部门加人成功')
    else:
        return get_result(False, u'只有管理员、部门主管、部门主管助手、父级部门主管、父级部门主管助手可以添加部门成员')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def remove_person_group(request, org_id, user_id, person, group):
    """
    部门加人
    :param group:
    :param person:
    :param user_id:
    :param request:
    :param org_id:
    :return:
    部门加人
    by:王健 at:2016-04-27
    部门变动事件
    by:王健 at:2016-05-03
    """
    if check_person_group_permiss(person, group):

        try:
            group.copy_old()
            member = Person.objects.get(org_id=org_id, user_id=user_id, is_active=True)
            if group.charge_id == member.id:
                if group.aide_id == person.id:
                    return get_result(False, u'主管助理,不能移除主管')
                group.charge = None
            if group.aide_id == member.id:
                group.aide = None

            group.members.remove(member)

            created, diff = group.compare_old()
            if diff:
                group.save()
            clean_organization_groups_cache(org_id)
            org_commend("org_group_change", org_id, None)
            if group.talkgroup_id:
                talkuser, created = TalkUser.objects.get_or_create(talkgroup_id=group.talkgroup_id, user_id=user_id)
                talkuser.copy_old()
                talkuser.is_active = False
                crea, diff = talkuser.compare_old()
                if diff:
                    talkuser.save()
                    talkuser.push_im_event(request.user)
                    im_commend("im_group_change", group.talkgroup_id)
        except Person.DoesNotExist:
            pass

        return get_result(True, u'部门成员移出成功')
    else:
        return get_result(False, u'只有管理员、部门主管、部门主管助手、父级部门主管、父级部门主管助手可以移出部门成员')


@check_request_parmes(org_id=("组织id", "r,int"), user_id=("用户id", "r,int"), realname=("姓名", ""), title=("职务", ""),
                      email=("电子邮件", "email"), is_gaoguan=("是否高管", "b", False), is_show_tel=("是否显示手机号", "b", True),
                      is_show_email=("是否显示邮箱", "b", True))
@client_login_required
@check_org_relation()
def update_person_group(request, org_id, user_id, realname, title, email, is_gaoguan, is_show_tel, is_show_email,
                        person):
    """
    修改组织成员信息
    :param group:
    :param person:
    :param user_id:
    :param request:
    :param org_id:
    :return:
    部门加人
    by:王健 at:2016-04-27
    """
    if person.manage_type in [1, 2]:
        try:
            member = Person.objects.get(org_id=org_id, user_id=user_id, is_active=True)
            member.copy_old()
            member.realname = realname
            member.email = email
            member.title = title
            member.is_gaoguan = is_gaoguan
            member.is_show_tel = is_show_tel
            member.is_show_email = is_show_email
            created, diff = member.compare_old()
            if diff:
                member.save()
                org_commend("org_group_change", org_id, None)
            return get_result(True, u'成员信息修改成功', member)
        except Person.DoesNotExist:
            return get_result(False, u'成员不存在')

    else:
        return get_result(False, u'只有管理员可以设置成员信息')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "r,int"), page_index=("页码", "int", 1),
                      page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation()
@check_group()
def query_member_by_group_list(request, org_id, group_id, page_index, page_size, person, group):
    """
    查询部门成员列表
    :param page_size:
    :param page_index:
    :param org_id:
    :param request:
    :return:
    查询部门成员列表
    by:王健 at:2016-04-27
    """
    query = Person.objects.list_json().filter(is_active=True, group=group, org_id=org_id)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("部门id", "int"))
@client_login_required
@check_org_relation()
def get_org_or_group_contacts(request, org_id, group_id, person):
    """
    查询组织中的未部门成员
    :param group_id:
    :param org_id:
    :param request:
    :return:
    查询组织中的未部门成员
    by:王健 at:2016-04-27
    """
    group = get_organization_groups(org_id, group_id)
    group['my_person'] = person
    return get_result(True, None, group)
