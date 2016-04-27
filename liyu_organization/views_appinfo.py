#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/27 下午2:19
# file: views_appinfo.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyu_organization.models import OrgApp, Permissions, Person
from liyu_organization.org_tools import check_org_relation, check_org_manager_relation
from liyuoa.models import AppInfo, AppRole
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required


@check_request_parmes(org_id=("组织id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation
def query_appinfo_by_org_list(request, org_id, person, page_index, page_size):
    """
    查询组织的应用列表
    :param page_size:
    :param page_index:
    :param org_id:
    :param request:
    :return:
    查询组织的应用列表
    by:王健 at:2016-04-27
    """
    query = OrgApp.objects.list_json().filter(is_active=True, org_id=org_id, app__is_active=True)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(org_id=("组织id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@client_login_required
@check_org_relation
def query_not_used_appinfo_by_org_list(request, org_id, person, page_index, page_size):
    """
    查询组织的应用列表
    :param page_size:
    :param page_index:
    :param org_id:
    :param request:
    :return:
    查询组织的应用列表
    by:王健 at:2016-04-27
    """
    query = AppInfo.objects.list_json().filter(is_active=True).exclude(orgapp__is_active=True)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(org_id=("组织id", "r,int"), app_id=("应用id", "r,int"))
@client_login_required
@check_org_manager_relation
def add_appinfo(request, org_id, app_id, person):
    """
    添加应用到组织
    :param request:
    :param org_id:
    :return:
    添加应用到组织
    by:王健 at:2016-04-27
    """
    try:
        app = AppInfo.objects.get(pk=app_id)
        orgapp, created = OrgApp.objects.get_or_create(org_id=org_id, app_id=app_id)
        orgapp.copy_old()
        orgapp.is_active = True
        create, diff = orgapp.compare_old()
        if diff:
            orgapp.save()
        return get_result(True, u'添加应用到组织成功')
    except AppInfo.DoesNotExist:
        return get_result(False, u'应用不存在')


@check_request_parmes(org_id=("组织id", "r,int"), app_id=("应用id", "r,int"))
@client_login_required
@check_org_manager_relation
def remove_appinfo(request, org_id, app_id, person):
    """
    从组织中删除应用
    :param request:
    :param org_id:
    :return:
    从组织中删除应用
    by:王健 at:2016-04-27
    """
    try:
        orgapp = OrgApp.objects.get(org_id=org_id, app_id=app_id, is_active=True)
        orgapp.copy_old()
        orgapp.is_active = False
        create, diff = orgapp.compare_old()
        if diff:
            orgapp.save()
        return get_result(True, u'从组织中移出应用成功')
    except OrgApp.DoesNotExist:
        return get_result(False, u'组织中没有这个应用')
    except AppInfo.DoesNotExist:
        return get_result(False, u'应用不存在')


@check_request_parmes(org_id=("组织id", "r,int"), app_id=("应用id", "r,int"), user_id=("用户id组", "r,int"),
                      role_id=("角色", "int"))
@client_login_required
@check_org_manager_relation
def make_appinfo_permission(request, org_id, app_id, user_id, role_id, person):
    """
    从组织中删除应用
    :param request:
    :param org_id:
    :return:
    从组织中删除应用
    by:王健 at:2016-04-27
    """
    try:
        org = person.org
        app = AppInfo.objects.get(pk=app_id, orgapp__org_id=org_id, is_active=True, orgapp__is_active=True)
        person = Person.objects.get(org_id=org_id, user_id=user_id, is_active=True)
        permission, created = Permissions.objects.get_or_create(org=org, person=person, app=app)
        permission.copy_old()
        if role_id is None:
            permission.is_active = False
        else:
            permission.role = AppRole.objects.get(app_id=app_id, pk=role_id, is_active=True)
        create, diff = permission.compare_old()
        if diff:
            permission.save()
        return get_result(True, u'修改用户在应用中的角色成功')
    except OrgApp.DoesNotExist:
        return get_result(False, u'组织中没有这个应用')
    except AppInfo.DoesNotExist:
        return get_result(False, u'应用不存在')
    except Person.DoesNotExist:
        return get_result(False, u'用户不是组织的成员')
    except AppRole.DoesNotExist:
        return get_result(False, u'应用中不存在这个角色')


@check_request_parmes(org_id=("组织id", "r,int"), user_ids=("用户id", "r,[int]"), app_ids=("应用id", "r,[int]"),
                      page_index=("页码", "int", 1), page_size=("页长度", "int", 200))
@client_login_required
def query_user_permissions_list(request, org_id, user_ids, app_ids, page_index, page_size):
    """
    查询用户对应应用的权限列表
    :param page_size:
    :param page_index:
    :param org_id:
    :param request:
    :return:
    查询用户对应应用的权限列表
    by:王健 at:2016-04-27
    """
    query = Permissions.objects.filter(is_active=True,person__user_id__in=user_ids, app_id__in=app_ids)
    query = query.values("org_id", 'person__user_id', 'app_id', 'role_id')

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(app_ids=("应用id", "r,[int]"), page_index=("页码", "int", 1), page_size=("页长度", "int", 200))
@client_login_required
def query_role_by_apps_list(request, app_ids, page_index, page_size):
    """
    查询应用的角色列表
    :param page_size:
    :param page_index:
    :param app_ids:
    :param request:
    :return:
    查询应用的角色列表
    by:王健 at:2016-04-27
    """
    query = AppRole.objects.list_json(['app_id']).filter(is_active=True, app_id__in=app_ids)
    return get_result(True, None, query.get_page(page_index, page_size))

