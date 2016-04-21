#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/21 上午11:49
# file:views_develop.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyuoa.models import AppApi, AppInfo, AppApiCareUser
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes


def query_all_app(request):
    """
    查询所有的app list信息
    :param request:
    :param :
    :return:
    查询所有的app list信息
    by:王健 at:2016-04-21
    """
    query_app = AppInfo.objects.list_json().filter(is_active=True).order_by('name')
    app_list = []
    app_dict = {}
    for app in query_app:
        app_list.append(app)
        app_dict[app['id']] = app
        app['apilist'] = []

    api_dict = {}
    for api in AppApi.objects.list_json(ex_parms=['app_id']).filter(app__is_active=True, is_active=True).order_by('url'):
        if app_dict.has_key(api['app_id']):
            app_dict[api['app_id']]['apilist'].append(api)
            api_dict[api['id']] = api
            api['is_confirm'] = False

    for apicare in AppApiCareUser.objects.values('api_id').filter(is_confirm=True, api__is_active=True,
                                                                                api__app__is_active=True):
        if api_dict.has_key(apicare['api_id']):
            apicare['api_id']['is_confirm'] = True

    return get_result(True, u'', app_list)


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
    by:王健 at:2016-04-21
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


@check_request_parmes(api_id=("接口id", "r,int"))
def get_api(request, api_id):
    """
    查询接口信息
    :param api_id:
    :param request:
    :return:
    查询接口信息
    by:王健 at:2016-04-21
    """
    try:
        obj = AppApi.objects.get_serializer(pk=api_id)
        return get_result(True, None, obj)
    except AppApi.DoesNotExist:
        return get_result(False, u'接口不存在')
