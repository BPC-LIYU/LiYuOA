# coding=utf-8
# Date: 11-12-8
# Time: 下午10:28
import datetime
import json
import re

from django.conf import settings
from django.core.paginator import Page
from django.db.models import QuerySet

from liyuoa.models import AppApiResponse
from util.jsonresult import get_result, JSONHttpResponse

__author__ = u'王健'


def client_admin_login_required(func=None):
    """
    系统管理员校验
    by:王健 at:2015-05-12
    优化管理员登陆校验
    by:王健 at:2015-05-12
    取消权限判断逻辑
    by: 范俊伟 at:2015-08-26
    :param func:
    :return:
    """

    def test(request, *args, **kwargs):
        if not request.user.is_anonymous():
            return func(request, *args, **kwargs)
        else:
            return get_result(False, u'请先登录', None, 1)

    return test


def client_login_required(func=None):
    """
    登录校验
    by:王健 at:2015-1-3
    添加手机号判断
    by:王健 at:2015-1-15
    修改逻辑
    by:尚宗凯 at:2015-3-26
    :param func:
    :return:
    """

    def test(request, *args, **kwargs):
        if not request.user.is_anonymous():
            if request.user.is_active:
                return func(request, *args, **kwargs)
            else:
                return get_result(False, u'用户已被禁用。', None, 5)
        else:
            return get_result(False, u'请先登录', None, 1)

    return test


def post_to_method_parmes(parms):
    """
    post参数转函数参数
    by: 范俊伟 at:2015-08-24
    :param parms: 参数名数组
    :return:
    """

    def post_to_method_parmes_func(func=None):
        def test(request, *args, **kwargs):
            for i in parms:
                kwargs[i] = request.REQUEST.get(i)
            return func(request, *args, **kwargs)

        return test

    return post_to_method_parmes_func


def request_parmes_value_check(name, value, check):
    """
    参数校验
    by: 范俊伟 at:2015-08-24
    增加以豆号分隔的int校验
    by: 范俊伟 at:2015-09-06
    增加email验证 和 电话号码验证
    by: 刘奕辰 at:2015-09-16
    :param name:
    :param value:
    :param check:
    :return:
    """
    if check == 'r':
        if not value:
            return "%s不能为空" % name, None
    elif check == 'int':
        if value:
            try:
                return None, int(value)
            except:
                return "%s应为整数" % name, None
    elif check == '[int]':  # 逗号分隔的int值
        if value:
            try:
                return None, [int(x) for x in value.strip(',').split(',') if x]
            except:
                return "%s应为逗号分隔的整数" % name, None
    elif check == 'email':
        if value:
            if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", value) is None:
                return "%s应为email格式" % name, None
    elif check == 'phone':
        if value:
            if re.match("^[\d\-]*$", value) is None:
                return "%s应为电话号码" % name, None
    elif check == 'json':
        if value:
            try:
                return None, json.loads(value)
            except:
                return "%s应为整数" % name, None

    return None, value


def check_request_parmes(**checks):
    """
    post参数转函数参数
    by: 范俊伟 at:2015-08-24
    :param checks:检测条件 例如:校验项目id不能为空 @check_request_parmes(project_id=('项目iD', 'r'))
    :return:
    """

    def check_request_parmes_func(func=None):
        def test(request, *args, **kwargs):
            errors = []
            for key, parm in checks.items():
                name = parm[0]
                value = request.POST.get(key)
                if not value:
                    value = request.GET.get(key)
                check_args = parm[1].split(',')
                for check in check_args:
                    if settings.DEBUG:
                        name = '(%s:%s)' % (key, name)
                    error, v = request_parmes_value_check(name, value, check)
                    kwargs[key] = v
                    if error:
                        errors.append(error)
                if value is None and len(parm) == 3:
                    kwargs[key] = parm[2]

            if errors:
                return get_result(False, ','.join(errors), None)
            if settings.DEBUG:
                response = func(request, *args, **kwargs)
                if isinstance(response, JSONHttpResponse) and response.is_response_suggest:
                    result = response.json['result']
                    data = None
                    if isinstance(result, dict):
                        if result.has_key('list') and result.has_key('page_index') and result.has_key('page_count'):
                            if len(result['list']) > 0:
                                data = result['list'][0]
                        else:
                            data = result
                    elif isinstance(result, Page):
                        if len(result) > 0:
                            data = result[0]
                    elif isinstance(result, list):
                        if len(result) > 0:
                            data = result[0]
                    if data:
                        fun_str = []
                        for key, value in data.items():
                            try:
                                if key != 'id':
                                    apiresponse = AppApiResponse.objects.filter(name=key, is_active=True,
                                                                                api__is_active=True,
                                                                                api__app__is_active=True)[0]
                                    title = apiresponse.title
                                else:
                                    title = ''
                            except IndexError:
                                title = ''
                            if isinstance(value, int):
                                fun_str.append('%s=("%s", "int")' % (key, title))
                            elif isinstance(value, datetime.datetime):
                                fun_str.append('%s=("%s", "datetime")' % (key, title))
                            elif isinstance(value, datetime.date):
                                fun_str.append('%s=("%s", "date")' % (key, title))
                            elif isinstance(value, datetime.time):
                                fun_str.append('%s=("%s", "time")' % (key, title))
                            elif isinstance(value, (list, QuerySet)):
                                fun_str.append('%s=("%s", "list")' % (key, title))
                            elif isinstance(value, dict):
                                fun_str.append('%s=("%s", "dict")' % (key, title))
                            elif key.rfind('_id') == len(key) - 3:
                                fun_str.append('%s=("%s", "int")' % (key, title))
                            else:
                                fun_str.append('%s=("%s", "")' % (key, title))
                        fun_str.sort()
                        print "%s——@check_response_results(%s)" % (request.META.get('PATH_INFO'), ', '.join(fun_str))
                        print ''
                return response
            else:
                return func(request, *args, **kwargs)

        return test

    return check_request_parmes_func


def check_response_results(**checks):
    """
    检测返回值
    by:王健 at:2016-04-22
    :param checks:检测条件 例如:校验项目id不能为空 @check_response_results(project_id=('项目iD', 'r'))
    :return:
    url以_list结尾时,返回值必须是数组
    by:王健 at:2016-04-23
    """

    def check_response_results_func(func=None):
        def check_response(request, *args, **kwargs):

            response = func(request, *args, **kwargs)
            if not settings.DEBUG:
                return response
            errors = []
            url = request.META.get('PATH_INFO')
            if url.rfind('_list') == len(url) - 5:
                response_type = 'list'
            else:
                response_type = 'dict'
            if isinstance(response, JSONHttpResponse):
                # 如果接口返回不成功,则不校验返回值
                if not response.json['success']:
                    return response
                result = response.json['result']
                data = None
                if isinstance(result, dict):
                    if result.has_key('list') and result.has_key('page_index') and result.has_key('page_count'):
                        if len(result['list']) > 0:
                            data = result['list'][0]
                            if response_type != 'list':
                                errors.append('返回值为list,但是url没有以_list结尾')
                    else:
                        data = result
                        if response_type != 'dict':
                            errors.append('返回值为dict,但是url却以_list结尾')
                elif isinstance(result, Page):
                    if len(result) > 0:
                        data = result[0]
                        if response_type != 'list':
                            errors.append('返回值为list,但是url没有以_list结尾')
                elif isinstance(result, list):
                    if len(result) > 0:
                        data = result[0]
                        if response_type != 'list':
                            errors.append('返回值为list,但是url没有以_list结尾')
                if data:
                    for key, parm in checks.items():
                        name = parm[0]
                        name = '(%s:%s)' % (key, name)
                        value = data.get(key, None)
                        error, v = request_parmes_value_check(name, data.has_key(key), 'r')
                        if error:
                            errors.append(error)
                        check_args = parm[1].split(',')
                        for check in check_args:
                            error, v = request_parmes_value_check(name, value, check)
                            if error:
                                errors.append(error)
                    lkey = list(set(data.keys()) - set(checks.keys()))
                    if lkey:
                        errors.append('缺少字段校验:%s' % ','.join(lkey))
                    if len(checks) > 0 and len(errors) == 0:
                        response.is_response_suggest = False
            if errors:
                return get_result(False, '%s:%s' % (url, ','.join(errors)), None)
            return response

        return check_response

    return check_response_results_func
