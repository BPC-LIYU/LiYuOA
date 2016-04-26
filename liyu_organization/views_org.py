#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/26 下午1:41
# file: views_org.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyu_organization.models import Organization, OrgApply
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



# todo:/同意加入组织/拒绝加入组织/把用户加入组织/把用户移出组织/添加管理员/删除管理员/转让组织/
# todo:/创建分组/修改分组信息(名称\隶属\主管\助手)/删除分组/分组加人/分组删人/修改成员信息(昵称\职务)/
# todo:/获取组织中的应用/添加组织中的应用/删除组织中的应用/设置应用和用户的权限/查询用户和应用的权限/
