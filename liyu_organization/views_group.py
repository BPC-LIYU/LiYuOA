#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/27 上午10:16
# file: views_group.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyu_organization.models import Group, Person
from liyu_organization.org_tools import check_org_relation, check_group, get_organization_groups, \
    clean_organization_groups_cache
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required


@check_request_parmes(org_id=("组织id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation()
def query_group_by_org_list(request, org_id, page_index, page_size, person):
    """
    查询组织中的分组列表,顶级分组
    :param person:
    :param page_size:
    :param page_index:
    :param org_id:
    :param request:
    :return:
    查询组织中的分组列表
    by:王健 at:2016-04-27
    """
    query = Group.objects.list_json().filter(is_active=True)

    query = query.filter(org_id=org_id, parent=None)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"), page_index=("页码", "int", 1),
                      page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation()
def query_group_by_group_list(request, org_id, group_id, page_index, page_size, person):
    """
    查询组织中的分组列表,顶级分组
    :param group_id:
    :param person:
    :param page_size:
    :param page_index:
    :param org_id:
    :param request:
    :return:
    查询组织中的分组列表
    by:王健 at:2016-04-27
    """
    query = Group.objects.list_json().filter(is_active=True)

    query = query.filter(org_id=org_id, parent_id=group_id)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(page_index=("页码", "int", 1), page_size=("页长度", "int", 200))
@client_login_required
def query_group_by_my_list(request, page_index, page_size):
    """
    查询组织中的分组列表,顶级分组
    :param page_size:
    :param page_index:
    :param request:
    :return:
    查询组织中的分组列表
    by:王健 at:2016-04-27
    """
    query = Group.objects.list_json().filter(is_active=True)

    query = query.filter(members=request.user.id)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "int"), name=("分组名称", ""), charge_id=("主管id", "int"), aide_id=("主管id", "int"))
@client_login_required
@check_org_relation()
def create_group(request, org_id, group_id, charge_id, aide_id, name, person):
    """
    创建分组
    :param request:
    :param org_id:
    :return:
    创建分组
    by:王健 at:2016-04-27
    创建分组时可以提供主管 和 主管助理的参数
    by:王健 at:2016-04-29
    """
    group = None
    if group_id is None:
        if person.manage_type not in [1, 2]:
            return get_result(False, u'只有管理员才能创建一级分组')
    else:
        try:
            group = Group.objects.get(org_id=org_id, pk=group_id, is_active=True)
        except Group.DoesNotExist:
            return get_result(False, u'分组不存在,不能创建子分组')
        if person.manage_type not in [1,
                                      2] and group.charge.user_id != request.user_id and group.aide.user_id != request.user_id:
            return get_result(False, u'只有管理员、分组主管、分组主管助手 可以创建自分组')

    newgroup = Group()
    newgroup.org_id = org_id
    newgroup.name = name
    newgroup.parent = group
    if group is not None and (group.charge.user_id == request.user_id or group.aide.user_id == request.user_id):
        newgroup.charge_id = group.charge_id
        newgroup.aide_id = group.aide_id

    if charge_id:
        newgroup.charge_id = charge_id
    if aide_id:
        newgroup.aide_id = aide_id

    newgroup.save()

    return get_result(True, u'创建分组成功', newgroup)


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"), name=("分组名称", ""),
                      icon_url=("头像", "url"), parent_id=("父级分组id", "int"))
@client_login_required
@check_org_relation()
@check_group()
def update_group(request, org_id, group_id, name, icon_url, parent_id, person, group):
    """
    修改分组的信息
    :param request:
    :param org_id:
    :return:
    修改分组的信息
    by:王健 at:2016-04-27
    """
    if person.manage_type in [1,
                              2] or group.charge.user_id == request.user.id or group.aide.user_id != request.user.id or (
                    group.parent_id is not None and (
                            group.parent.charge.user_id == request.user.id or group.parent.aide.user_id == request.user.id)):
        pass
    else:
        return get_result(False, u'只有管理员、分组主管、分组主管助手、父级分组主管、父级分组主管助手可以修改分组信息')
    try:
        if parent_id is not None:
            parentgroup = Group.objects.get(org_id=org_id, pk=parent_id, is_active=True)
    except Group.DoesNotExist:
        return get_result(False, u'设置的父级分组不存在,无法修改')

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

    return get_result(True, u'修改分组信息成功', group)


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def remove_charge_group(request, org_id, person, group):
    """
    删除分组主管
    :param request:
    :param org_id:
    :return:
    删除分组主管
    by:王健 at:2016-04-27
    """
    if person.manage_type in [1,
                              2] or group.charge.user_id == request.user.id or group.aide.user_id != request.user.id or (
                    group.parent_id is not None and (
                            group.parent.charge.user_id == request.user.id or group.parent.aide.user_id == request.user.id)):
        group.copy_old()
        group.charge = None
        created, diff = group.compare_old()
        if diff:
            group.save()
        return get_result(True, u'删除分组主管成功', group)
    else:
        return get_result(False, u'只有管理员、分组主管、分组主管助手、父级分组主管、父级分组主管助手可以修改分组信息')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def remove_aide_group(request, org_id, person, group):
    """
    删除分组主管
    :param request:
    :param org_id:
    :return:
    删除分组主管
    by:王健 at:2016-04-27
    """
    if person.manage_type in [1,
                              2] or group.charge.user_id == request.user.id or group.aide.user_id != request.user.id or (
                    group.parent_id is not None and (
                            group.parent.charge.user_id == request.user.id or group.parent.aide.user_id == request.user.id)):
        group.copy_old()
        group.aide = None
        created, diff = group.compare_old()
        if diff:
            group.save()
        return get_result(True, u'删除分组主管助手成功', group)
    else:
        return get_result(False, u'只有管理员、分组主管、分组主管助手、父级分组主管、父级分组主管助手可以修改分组信息')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def add_charge_group(request, org_id, group_id, user_id, person, group):
    """
    添加分组主管
    :param request:
    :param org_id:
    :return:
    删除分组主管
    by:王健 at:2016-04-27
    """
    if person.manage_type in [1, 2] or group.charge.user_id == request.user.id or (
                    group.parent_id is not None and (
                            group.parent.charge.user_id == request.user.id or group.parent.aide.user_id == request.user.id)):
        group.copy_old()
        try:
            group.charge = Person.objects.get(org_id=org_id, user_id=user_id, is_active=True)
        except Person.DoesNotExist:
            return get_result(False, u'用户不是当前组织的成员,不能设置成主管')
        created, diff = group.compare_old()
        if diff:
            group.save()
        return get_result(True, u'设置分组主管成功', group)
    else:
        return get_result(False, u'只有管理员、分组主管、父级分组主管、父级分组主管助手可以添加分组主管')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def add_aide_group(request, org_id, user_id, person, group):
    """
    删除分组主管
    :param group:
    :param person:
    :param user_id:
    :param request:
    :param org_id:
    :return:
    删除分组主管
    by:王健 at:2016-04-27
    """
    if person.manage_type in [1,
                              2] or group.charge.user_id == request.user.id or group.aide.user_id == request.user.id or (
                    group.parent_id is not None and (
                            group.parent.charge.user_id == request.user.id or group.parent.aide.user_id == request.user.id)):

        group.copy_old()
        try:
            group.aide = Person.objects.get(org_id=org_id, user_id=user_id, is_active=True)
        except Person.DoesNotExist:
            return get_result(False, u'用户不是当前组织的成员,不能设置成主管助手')
        created, diff = group.compare_old()
        if diff:
            group.save()
        return get_result(True, u'设置分组主管助手成功', group)
    else:
        return get_result(False, u'只有管理员、分组主管、分组主管助手、父级分组主管、父级分组主管助手可以添加分组主管助手')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def remove_group(request, org_id, person, group):
    """
    删除分组
    :param group:
    :param person:
    :param request:
    :param org_id:
    :return:
    删除分组
    by:王健 at:2016-04-27
    """
    if person.manage_type in [1, 2] or group.charge.user_id == request.user.id or (group.parent_id is not None and (
                    group.parent.charge.user_id == request.user.id or group.parent.aide.user_id == request.user.id)):

        group.copy_old()
        group.is_active = False
        created, diff = group.compare_old()
        if diff:
            group.save()
        return get_result(True, u'删除分组成功', group)
    else:
        return get_result(False, u'只有管理员、分组主管、父级分组主管、父级分组主管助手可以删除分组')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def add_person_group(request, org_id, user_id, person, group):
    """
    分组加人
    :param group:
    :param person:
    :param user_id:
    :param request:
    :param org_id:
    :return:
    分组加人
    by:王健 at:2016-04-27
    """
    if person.manage_type in [1,
                              2] or group.charge.user_id == request.user.id or group.aide.user_id == request.user.id or (
                    group.parent_id is not None and (
                            group.parent.charge.user_id == request.user.id or group.parent.aide.user_id == request.user.id)):

        try:
            group.members.add(Person.objects.get(org_id=org_id, user_id=user_id, is_active=True))
        except Person.DoesNotExist:
            return get_result(False, u'用户不是当前组织的成员,不能加入分组')
        clean_organization_groups_cache(org_id)
        return get_result(True, u'分组加人成功')
    else:
        return get_result(False, u'只有管理员、分组主管、分组主管助手、父级分组主管、父级分组主管助手可以添加分组成员')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
@check_group()
def remove_person_group(request, org_id, user_id, person, group):
    """
    分组加人
    :param group:
    :param person:
    :param user_id:
    :param request:
    :param org_id:
    :return:
    分组加人
    by:王健 at:2016-04-27
    """
    if person.manage_type in [1,
                              2] or group.charge.user_id == request.user.id or group.aide.user_id == request.user.id or (
                    group.parent_id is not None and (
                            group.parent.charge.user_id == request.user.id or group.parent.aide.user_id == request.user.id)):

        try:
            group.members.remove(Person.objects.get(org_id=org_id, user_id=user_id, is_active=True))
        except Person.DoesNotExist:
            pass
        clean_organization_groups_cache(org_id)

        return get_result(True, u'分组成员移出成功')
    else:
        return get_result(False, u'只有管理员、分组主管、分组主管助手、父级分组主管、父级分组主管助手可以移出分组成员')


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
    分组加人
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
            return get_result(True, u'成员信息修改成功', member)
        except Person.DoesNotExist:
            return get_result(False, u'成员不存在')

    else:
        return get_result(False, u'只有管理员可以设置成员信息')


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"), page_index=("页码", "int", 1),
                      page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation()
@check_group()
def query_member_by_group_list(request, org_id, group_id, page_index, page_size, person, group):
    """
    查询分组成员列表
    :param page_size:
    :param page_index:
    :param org_id:
    :param request:
    :return:
    查询分组成员列表
    by:王健 at:2016-04-27
    """
    query = Person.objects.list_json().filter(is_active=True, group=group, org_id=org_id)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "int"))
@client_login_required
def get_org_or_group_contacts(request, org_id, group_id):
    """
    查询组织中的未分组成员
    :param group_id:
    :param org_id:
    :param request:
    :return:
    查询组织中的未分组成员
    by:王健 at:2016-04-27
    """

    return get_result(True, None, get_organization_groups(org_id, group_id))
