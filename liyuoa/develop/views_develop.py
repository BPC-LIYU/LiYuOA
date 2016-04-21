#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/21 上午11:49
# file:views_develop.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyuoa.models import AppApi, AppInfo, AppApiCareUser
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes


@check_request_parmes(app_id=("应用id", 'int'), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
def query_api_list(request, app_id, page_index, page_size):
    """
    查询接口文档列表
    :param page_size:
    :param page_index:
    :param app_id:
    :param request:
    :return:
    查询接口,分页
    by:王健 at:2016-04-21
    """
    query = AppApi.objects.list_json().filter(is_active=True, app__is_active=True)

    if app_id is not None:
        query = query.filter(app_id=app_id)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
def query_appinfo_list(request, page_index, page_size):
    """
    查询接口文档列表
    :param page_size:
    :param page_index:
    :param app_id:
    :param request:
    :return:
    查询接口,分页
    by:王健 at:2016-04-21
    """
    query = AppInfo.objects.list_json().filter(is_active=True)

    return get_result(True, None, query.get_page(page_index, page_size))


@check_request_parmes(appinfo_id=("应用信息id", "r,int"))
def get_appinfo(request, appinfo_id):
    """
    查询应用信息
    :param appinfo_id:
    :param request:
    :return:
    查询应用信息
    by:王健 at:
    """
    try:
        obj = AppInfo.objects.get_serializer(pk=appinfo_id)
        return get_result(True, None, obj)
    except AppInfo.DoesNotExist:
        return get_result(False, u'应用不存在')


@check_request_parmes(api_id=("应用id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
def query_appcareuser_list(request, api_id, page_index, page_size):
    """
    查询接口关注列表
    :param page_size:
    :param page_index:
    :param api_id:
    :param request:
    :return:
    查询接口关注列表
    by:王健 at:2016-04-21
    """
    query = AppApiCareUser.objects.list_json().filter(is_active=True)

    if api_id is not None:
        query = query.filter(api_id=api_id)

    return get_result(True, None, query.get_page(page_index, page_size))
