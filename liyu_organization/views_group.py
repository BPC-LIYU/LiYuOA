#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/27 上午10:16
# file: views_group.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyu_organization.models import Group
from liyu_organization.org_tools import check_org_relation
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required


@check_request_parmes(org_id=("组织id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation
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


@check_request_parmes(org_id=("组织id", "r,int"), group_id=("分组id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation
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


@check_request_parmes(org_id=("组织id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation
def query_group_by_my_list(request, org_id, page_index, page_size, person):
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

    query = query.filter(org_id=org_id, members=request.user.id)

    return get_result(True, None, query.get_page(page_index, page_size))


# todo:/创建分组/修改分组信息(名称\隶属\主管\助手)/删除分组/分组加人/分组删人/修改成员信息(昵称\职务)/
# todo:/获取组织中的应用/添加组织中的应用/删除组织中的应用/设置应用和用户的权限/查询用户和应用的权限/
