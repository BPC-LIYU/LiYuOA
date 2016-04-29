#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/26 下午1:41
# file: views_org.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyu_organization.models import Organization, OrgApply, Person, OrgHeadIcon
from liyu_organization.org_tools import check_org_relation, check_org_manager_relation, org_commend
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required


@check_request_parmes(page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
def query_my_org_list(request, page_index, page_size):
    """
    查询我的组织列表
    :param page_size:
    :param page_index:
    :param :
    :param request:
    :return:
    查询我的组织列表
    by:王健 at:2016-04-26
    """
    query = Organization.objects.list_json().filter(person__user=request.user, person__is_active=True).filter(
        is_active=True)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(org_id=("组织id", "r,int"))
@client_login_required
def get_organization(request, org_id):
    """
    查询组织信息信息
    :param org_id:
    :param request:
    :return:
    查询组织信息信息
    by:王健 at:2016-04-26
    """
    try:
        obj = Organization.objects.get_serializer(pk=org_id)
        return get_result(True, None, obj)
    except Organization.DoesNotExist:
        return get_result(False, u'组织不存在')


@check_request_parmes(name=("组织名称", "r"), icon_url=("组织头像", "url"))
@client_login_required
def create_organization(request, name, icon_url):
    """
    创建组织
    :param icon_url:
    :param name:
    :param request:
    :return:
    创建组织
    by:王健 at:2016-04-26
    """
    try:
        obj = Organization()
        obj.name = name
        obj.icon_url = icon_url
        obj.save()
        person = Person()
        person.org = obj
        person.manage_type = 2
        person.user = request.user
        person.realname = request.user.realname
        person.email = request.user.email
        person.save()

        org_commend("create_organization", obj.id, None)

        return get_result(True, None, obj)
    except Organization.DoesNotExist:
        return get_result(False, u'组织不存在')


@check_request_parmes(org_id=("组织id", "r,int"), name=("组织名称", "r"), icon_url=("组织头像", "url"))
@client_login_required
def update_organization(request, org_id, name, icon_url):
    """
    查询组织信息信息
    :param org_id:
    :param request:
    :return:
    查询组织信息信息
    by:王健 at:2016-04-26
    """
    try:
        obj = Organization.objects.get(pk=org_id)
        obj.copy_old()
        obj.name = name
        if icon_url:
            obj.icon_url = icon_url
        created, diff = obj.compare_old()
        if diff:
            obj.save()
            org_commend("update_organization", obj.id, None)
        return get_result(True, None, obj)
    except Organization.DoesNotExist:
        return get_result(False, u'组织不存在')


@check_request_parmes(org_id=("组织id", "r,int"), content=("申请内容", "r"))
@client_login_required
def apply_organization(request, org_id, content):
    """
    申请加入组织
    :param content:
    :param request:
    :param org_id:
    :return:
    申请加入组织
    by:王健 at:2016-04-26
    """
    applyorg = OrgApply()
    applyorg.user = request.user
    applyorg.org_id = org_id
    applyorg.content = content
    applyorg.save()

    return get_result(True, u'已经发出申请,等待组织管理员审核', applyorg)


@check_request_parmes(org_id=("组织id", "r,int"), orgapply_id=("申请id", "r,int"))
@client_login_required
@check_org_manager_relation()
def agree_organization(request, org_id, orgapply_id, person):
    """
    同意加入组织
    :param orgapply_id:
    :param person:
    :param request:
    :param org_id:
    :return:
    同意加入组织
    by:王健 at:2016-04-27
    """
    try:
        apporg = OrgApply.objects.get(id=orgapply_id, org_id=org_id)
        if apporg.status != 0:
            if apporg.status == 1:
                return get_result(False, u'该申请已经被 %s 通过' % apporg.checker)
            elif apporg.status == 2:
                return get_result(False, u'该申请已经被 %s 拒绝' % apporg.checker)
            else:
                return get_result(False, u'该申请已经被 %s 处理' % apporg.checker)

        apporg.copy_old()
        apporg.status = 1
        apporg.compare_old()
        apporg.save()
        member, created = Person.objects.get_or_create(user_id=apporg.user_id, org_id=org_id)
        member.copy_old()
        member.realname = apporg.user.realname
        member.email = apporg.user.email
        member.is_active = True
        member.manage_type = 0
        create, diff = member.compare_old()
        if diff:
            member.save()
        return get_result(True, u'已同意用户的加入组织申请', apporg)
    except OrgApply.DoesNotExist:
        return get_result(False, u'这不是发给您的组织的申请,您不能处理')


@check_request_parmes(org_id=("组织id", "r,int"), orgapply_id=("申请id", "r,int"))
@client_login_required
@check_org_manager_relation()
def reject_organization(request, org_id, orgapply_id, person):
    """
    拒绝加入组织
    :param orgapply_id:
    :param person:
    :param request:
    :param org_id:
    :return:
    拒绝加入组织
    by:王健 at:2016-04-27
    """
    try:
        apporg = OrgApply.objects.get(id=orgapply_id, org_id=org_id)
        if apporg.status != 0:
            if apporg.status == 1:
                return get_result(False, u'该申请已经被 %s 通过' % apporg.checker)
            elif apporg.status == 2:
                return get_result(False, u'该申请已经被 %s 拒绝' % apporg.checker)
            else:
                return get_result(False, u'该申请已经被 %s 处理' % apporg.checker)

        apporg.copy_old()
        apporg.status = 2
        apporg.compare_old()
        apporg.save()
        return get_result(True, u'已经绝用户的加入组织申请', apporg)
    except OrgApply.DoesNotExist:
        return get_result(False, u'这不是发给您的组织的申请,您不能处理')


@check_request_parmes(org_id=("组织id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_manager_relation()
def add_person_org(request, org_id, user_id, person):
    """
    把用户加入组织,无需申请
    :param user_id:
    :param person:
    :param request:
    :param org_id:
    :return:
    把用户加入组织,无需申请
    by:王健 at:2016-04-27
    """
    member, created = Person.objects.get_or_create(user_id=user_id, org_id=org_id)
    member.copy_old()
    member.realname = member.user.realname
    member.email = member.user.email
    member.is_active = True
    member.manage_type = 0
    create, diff = member.compare_old()
    if diff:
        member.save()

    return get_result(True, u'成功将用户加入组织', member)


@check_request_parmes(org_id=("组织id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_manager_relation()
def remove_person_org(request, org_id, user_id, person):
    """
    把用户移出组织
    :param user_id:
    :param person:
    :param request:
    :param org_id:
    :return:
    把用户移出组织
    by:王健 at:2016-04-27
    """
    try:

        member = Person.objects.get(user_id=user_id, org_id=org_id)
        member.copy_old()
        member.is_active = False
        create, diff = member.compare_old()
        if diff:
            member.save()
        return get_result(True, u'成功将用户移出组织', member)
    except Person.DoesNotExist:
        return get_result(False, u'用户不是该组织成员')


@check_request_parmes(org_id=("组织id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
def add_manager_org(request, org_id, user_id, person):
    """
    添加管理员
    :param user_id:
    :param person:
    :param request:
    :param org_id:
    :return:
    添加管理员
    by:王健 at:2016-04-27
    """
    if person.manage_type == 2:
        return get_result(False, u'只有超级管理员才能添加管理员')
    try:

        member = Person.objects.get(user_id=user_id, org_id=org_id, is_active=True)
        member.copy_old()
        member.manage_type = 1
        create, diff = member.compare_old()
        if diff:
            member.save()
        return get_result(True, u'成功将用户设置成管理员', member)
    except Person.DoesNotExist:
        return get_result(False, u'用户不是该组织成员')


@check_request_parmes(org_id=("组织id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
def remove_manager_org(request, org_id, user_id, person):
    """
    移除管理员
    :param user_id:
    :param person:
    :param request:
    :param org_id:
    :return:
    移除管理员
    by:王健 at:2016-04-27
    """
    if person.manage_type == 2:
        return get_result(False, u'只有超级管理员才能移除管理员')
    try:

        member = Person.objects.get(user_id=user_id, org_id=org_id, is_active=True)
        member.copy_old()
        member.manage_type = 0
        create, diff = member.compare_old()
        if diff:
            member.save()
        return get_result(True, u'成功将用户设置成管理员', member)
    except Person.DoesNotExist:
        return get_result(False, u'用户不是该组织成员')


@check_request_parmes(org_id=("组织id", "r,int"), user_id=("用户id", "r,int"))
@client_login_required
@check_org_relation()
def transfer_manager_org(request, org_id, user_id, person):
    """
    添加新的超级管理员
    :param user_id:
    :param person:
    :param request:
    :param org_id:
    :return:
    添加新的超级管理员
    by:王健 at:2016-04-27
    """
    if person.manage_type == 2:
        return get_result(False, u'只有超级管理员才能添加新的超级管理员')
    try:

        member = Person.objects.get(user_id=user_id, org_id=org_id, is_active=True)
        member.copy_old()
        member.manage_type = 2
        create, diff = member.compare_old()
        if diff:
            member.save()

        return get_result(True, u'成功将用户设置成超级管理员', member)
    except Person.DoesNotExist:
        return get_result(False, u'用户不是该组织成员')


@check_request_parmes(org_id=("组织id", "r,int"), nsfile_id=("文件id", "r,int"))
@client_login_required
@check_org_manager_relation()
def create_org_headicon(request, org_id, nsfile_id, person):
    """
    上传组织头像
    :param person:
    :param request:
    :param org_id:
    :param nsfile_id:
    :return:
    添加文件id
    by:王健 at:2016-04-29
    """
    orghead = OrgHeadIcon()
    orghead.org_id = org_id
    orghead.person = person
    orghead.nsfile_id = nsfile_id
    orghead.save()
    orghead.org.icon_url = orghead.nsfile.get_thumbnail(orghead.nsfile.fileurl, orghead.nsfile.bucket,
                                                        orghead.nsfile.name, orghead.nsfile.filetype)
    orghead.org.save()
    return get_result(True, u'上传组织头像成功', orghead.org)
