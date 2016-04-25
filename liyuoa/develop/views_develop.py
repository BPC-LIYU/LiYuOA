#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/21 上午11:49
# file:views_develop.py
# Email: wangjian2254@icloud.com
# Author: 王健
from liyuoa.models import AppApi, AppInfo, AppApiCareUser, AppApiParameter, AppApiComment, AppApiResponse
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, check_response_results
from util.model_tools import page_obj_query


@check_request_parmes(page_index=("页码", "int", 1), page_size=("页长度", "int", 1000))
@check_response_results(apilist=("接口列表", "list"), flag=("应用flag", ""), id=("应用id", "int"), name=("接口名字", ""), type_flag=("应用类型", ""))
def query_all_app_list(request, page_index, page_size):
    """
    查询所有的app list信息
    :param page_size:
    :param page_index:
    :param request:
    :param :
    :return:
    查询所有的app list信息
    by:王健 at:2016-04-21
    改造成分页返回值
    by:王健 at:2016-04-23
    """
    query_app = AppInfo.objects.list_json().filter(is_active=True).order_by('name')
    app_list = []
    app_dict = {}
    for app in query_app:
        app_list.append(app)
        app_dict[app['id']] = app
        app['apilist'] = []

    api_dict = {}
    for api in AppApi.objects.list_json(ex_parms=['app_id']).filter(app__is_active=True, is_active=True).order_by(
            'create_time'):
        if app_dict.has_key(api['app_id']):
            app_dict[api['app_id']]['apilist'].append(api)
            api_dict[api['id']] = api
            api['is_confirm'] = False

    for apicare in AppApiCareUser.objects.values('api_id').filter(is_confirm=True, api__is_active=True,
                                                                  api__app__is_active=True):
        if api_dict.has_key(apicare['api_id']):
            apicare['api_id']['is_confirm'] = True

    return get_result(True, u'', page_obj_query(app_list, page_index, page_size))


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


@check_request_parmes(app_id=("应用id", 'r,int'), page_index=("页码", "int", 1), page_size=("页长度", "int", 20))
@check_response_results(code_content=("代码", ""), create_time=("创建时间", "datetime"), id=("接口id", "int"),
                        is_active=("是否可用", "int"), name=("接口名字", ""), namespace=("函数路径", ""),
                        parameterlist=("参数列表", "list"), response_type=("接口返回值类型", ""), responselist=("返回值列表", "list"),
                        update_time=("最后更新时间", "datetime"), url=("接口url", ""))
def query_api_detail_list(request, app_id, page_index, page_size):
    """
    查询接口文档详细信息列表带参数
    :param page_size:
    :param page_index:
    :param app_id:
    :param request:
    :return:
    查询接口,分页
    by:王健 at:2016-04-21
    查询接口文档详细信息列表带参数,分页
    by:王健 at:2016-04-22
    """
    query = AppApi.objects.detail_json().filter(is_active=True, app__is_active=True).order_by('create_time')

    query = query.filter(app_id=app_id)
    page = query.get_page(page_index, page_size)
    apilist = []
    apidict = {}
    for api in page:
        apilist.append(api)
        apidict[api['id']] = api
        api['parameterlist'] = []
        api['responselist'] = []

    for apiparm in AppApiParameter.objects.list_json().filter(api__app_id=app_id, api__is_active=True, is_active=True,
                                                              api__app__is_active=True):
        if apidict.has_key(apiparm['api_id']):
            apidict[apiparm['api_id']]['parameterlist'].append(apiparm)

    for apiresponse in AppApiResponse.objects.list_json().filter(api__app_id=app_id, api__is_active=True,
                                                                 is_active=True,
                                                                 api__app__is_active=True):
        if apidict.has_key(apiresponse['api_id']):
            apidict[apiresponse['api_id']]['responselist'].append(apiresponse)
    return get_result(True, None, {"list": apilist, 'page_index': page.number, "page_count": page.paginator.num_pages})


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
@check_response_results(create_time=("创建时间", "datetime"), desc=("应用备注", ""), flag=("应用flag", ""), id=("应用id", "int"),
                        is_active=("是否可用", "int"), is_show=("是否显示在应用中", "int"), name=("接口名字", ""), namespace=("模块", ""),
                        type_flag=("应用类型", ""))
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
@check_response_results(code_content=("代码", ""), create_time=("创建时间", "datetime"), id=("接口id", "int"),
                        is_active=("是否可用", "int"), name=("接口名称", ""), namespace=("函数路径", ""),
                        parameterlist=("参数列表", "list"), response_type=("接口返回值类型", ""), responselist=("返回值列表", "list"),
                        update_time=("最后更新时间", "datetime"), url=("接口url", ""))
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
        obj['parameterlist'] = []
        obj['responselist'] = []
        for apiparm in AppApiParameter.objects.list_json().filter(api_id=api_id, is_active=True):
            obj['parameterlist'].append(apiparm)
        for apiresponse in AppApiResponse.objects.list_json().filter(api_id=api_id, is_active=True):
            obj['responselist'].append(apiresponse)
        return get_result(True, None, obj)
    except AppApi.DoesNotExist:
        return get_result(False, u'接口不存在')


@check_request_parmes(api_id=("接口id", "r,int"))
@check_response_results(apicareuser=("api关注用户", "list"), code_content=("代码", ""), create_time=("创建时间", "datetime"),
                        id=("接口id", "int"), is_active=("是否可用", "int"), name=("接口名字", ""), namespace=("函数路径", ""),
                        parameterlist=("参数列表", "list"), update_time=("最后更新时间", "datetime"), url=("接口url", ""),
                        response_type=("接口返回值类型", ""), responselist=("返回值列表", "list"))
def get_api_detail(request, api_id):
    """
    查询接口详细信息, 带修改历史记录
    :param api_id:
    :param request:
    :return:
    查询接口详细信息
    by:王健 at:2016-04-22
    """
    try:
        obj = AppApi.objects.get_serializer(pk=api_id)
        obj['parameterlist'] = []
        obj['responselist'] = []
        for apiparm in AppApiParameter.objects.list_json().filter(api_id=api_id, is_active=True):
            obj['parameterlist'].append(apiparm)
        obj['apicareuser'] = []
        for careuser in AppApiCareUser.objects.list_json().filter(api_id=api_id, is_active=True, user__is_active=True):
            obj['apicareuser'].append(careuser)
        for apiresponse in AppApiResponse.objects.list_json().filter(api_id=api_id, is_active=True):
            obj['responselist'].append(apiresponse)
        return get_result(True, None, obj)
    except AppApi.DoesNotExist:
        return get_result(False, u'接口不存在')


@check_request_parmes(api_id=("接口id", "r,int"), page_index=("页码", "int", 1), page_size=("页长度", "int", 2))
@check_response_results(user__icon_url=("用户头像url", ""), to_user__icon_url=("被评论用户头像", ""),
                        user_id=("用户id", "int"), username=("匿名用户名称", ""),
                        to_comment__user__realname=("被评论的评论的用户真实姓名", ""), api_id=("接口id", "int"),
                        content=("评论内容", ""), source=("评论来源", "int"), to_comment__user_id=("被评论的用户id", "int"),
                        create_time=("评论时间", "datetime"), to_comment_id=("被评论的id", "int"),
                        to_comment__content=("被评论的内容", ""), user__realname=("用户真实姓名", ""), id=("评论id", "int"),
                        to_comment__user__icon_url=("被评论的的评论的作者头像", ""), to_user__realname=("被评论的用户真实姓名", ""))
def query_apicomment_list(request, api_id, page_index, page_size):
    """
    查询接口评论列表
    :param page_size:
    :param page_index:
    :param api_id:
    :param request:
    :return:
    查询接口评论列表
    by:王健 at:2016-04-22
    """
    query = AppApiComment.objects.list_json().filter(is_active=True)

    query = query.filter(api_id=api_id)

    return get_result(True, None, query.get_page(page_index, page_size))
