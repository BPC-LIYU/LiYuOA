#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/21 下午4:00
# file: views_qrcode.py
# Email: wangjian2254@icloud.com
# Author: 王健
from urllib import urlencode

from django import http
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.cache import cache
from django.utils.crypto import get_random_string

from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required, check_response_results
from util.middleware import getHost


@check_request_parmes()
@check_response_results(state=("逻辑状态", ""))
def qrcode_login_check(request):
    """
    sessionid 在成功后返回给 客户端
    :param request:
    :return:
    sessionid 在成功后返回给 客户端
    by:王健 at:2016-04-05
    """
    sessionid = request.session.session_key
    if not sessionid:
        request.session.save()
        sessionid = request.session.session_key
    rand_code = request.session.get('desktop_qrcode_login_code')
    if not rand_code:
        return get_result(True, "", {"state": "reload"})
    cache_key = "dql_%s_%s" % (sessionid, rand_code)
    cache_parms = cache.get(cache_key)
    if not cache_parms:
        return get_result(True, "", {"state": "reload"})
    state = cache_parms.get("state")
    if state == "waite":
        return get_result(True, "", {"state": "waite"})
    elif state == "scan":
        return get_result(True, "", {"state": "scan"})
    elif state == "ok":
        user_id = cache_parms.get("user_id")
        user = authenticate(user_id=user_id)
        if user:
            auth_login(request, user)
            sessionid = request.session.session_key
            return get_result(True, "", {"state": "ok", "sessionid": sessionid})
        else:
            return get_result(True, "", {"state": "reload"})


@check_request_parmes(cache_key=("缓存键", 'r'), state=("逻辑状态", 'r'))
@check_response_results(state=("逻辑状态", ""))
@client_login_required
def qrcode_login_scan(request, cache_key, state):
    """
    扫码登录
    :param request:
    :param cache_key:
    :param state:
    :return:
    扫码登录
    by:王健 at:2016-04-21
    """
    cache_parms = cache.get(cache_key)
    if not cache_parms:
        return get_result(True, "", {"state": "reload"})
    if state == "scan":
        cache_parms['state'] = 'scan'
        cache.set(cache_key, cache_parms, 60 * 5)
    elif state == "ok":
        cache_parms['state'] = 'ok'
        cache_parms['user_id'] = request.user.id
        cache.set(cache_key, cache_parms, 60 * 5)
    return get_result(True, "", {"state": "ok"})


@check_request_parmes()
@check_response_results(text=("二维码数值", ""))
def qrcode_login_string(request):
    """
    生成登录二维码数值
    :param request:
    :return:
    生成登录的二维码数值
    by:王健 at:2016-04-21
    """
    sessionid = request.session.session_key
    if not sessionid:
        request.session.save()
        sessionid = request.session.session_key
    rand_code = get_random_string(length=6)
    cache_key = "dql_%s_%s" % (sessionid, rand_code)
    cache.set(cache_key, {"state": "waite", "user_id": None}, 60 * 5)
    request.session["desktop_qrcode_login_code"] = rand_code
    args = ['3', cache_key]
    p = '|'.join(args)
    parms = {"p": p}
    text = "http://%s/sys/qrcode2?%s" % (getHost(), urlencode(parms))
    return get_result(True, '', {"text": text})


@check_request_parmes(p=("扫码值", 'r'))
def qrcode_view2(request, p):
    """
    二维码处理函数 v2
    p 以|分割的函数
    [0]:action
    action:0 website [1]org_id
    action:1 user [1]user_id
    action:2 join_org [1]org_id
    action:3 desktop_login [1]code
    :param p:
    :param request:
    :return:
    """
    args = p.split('|')
    action = args[0]

    if action == "0":
        if len(args) != 2:
            return http.HttpResponse('len error')
        project_id = args[1]
        url = 'http://%s/ph/?project_id=%s' % (getHost(), project_id)
        return http.HttpResponseRedirect(url)
    elif action == "1":
        if len(args) != 2:
            return http.HttpResponse('len error')
        user_id = args[1]
        url = 'http://%s/ph/user_info?user_id=%s' % (getHost(), user_id)
        return http.HttpResponseRedirect(url)
    elif action == "2":
        if len(args) != 2:
            return http.HttpResponse('len error')
        project_id = args[1]
        url = 'http://%s/org/get_org_info?join=1&org_id=%s' % (getHost(), project_id)
        return http.HttpResponseRedirect(url)
    elif action == "3":
        if len(args) != 2:
            return http.HttpResponse('len error')
        code = args[1]
        url = 'http://www.ddbuild.cn'
        return http.HttpResponseRedirect(url)
    else:
        str = "未知action:%s" % action
    return http.HttpResponse(str)
