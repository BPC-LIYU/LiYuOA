# coding=utf-8
# Date: 11-12-8
# Time: 下午10:28
import json
import re

from util.jsonresult import get_result

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
                    error, v = request_parmes_value_check(name, value, check)
                    kwargs[key] = v
                    if error:
                        errors.append(error)
                if value is None and len(parm) == 3:
                    kwargs[key] = parm[2]

            if errors:
                return get_result(False, ','.join(errors), None)
            return func(request, *args, **kwargs)

        return test

    return check_request_parmes_func
