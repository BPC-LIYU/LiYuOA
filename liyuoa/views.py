#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/21 下午7:27
# file:app_config.py
# Email: wangjian2254@icloud.com
# Author: 王健
import time

from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate

from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, client_login_required
from util.tools import getUserIconUrl


def logout(request):
    """
    退出账号
    :param request:
    :return:
    退出
    by:王健 at:2016-04-21
    """
    auth_logout(request)
    return get_result(True, '')


def check_login(request):
    """
    检查是否登录
    :param request:
    :param :
    :return:
    检查是否登录
    by:王健 at:2016-04-21
    """
    sessionid = request.session.session_key
    if not sessionid:
        request.session.save()
        sessionid = request.session.session_key

    has_login = False
    if not request.user.is_anonymous():
        has_login = True

    return get_result(True, u'', {"has_login": has_login, "sessionid": sessionid})


@check_request_parmes(realname=("真实姓名", 'r'), username=("手机号", "r,phone"), password=("密码", "r"),
                      email=("电子邮箱", "email", ''), code=("验证码", "r,int"))
def reg_user(request, realname, username, password, email, code):
    """
    注册用户
    :param code:
    :param request:
    :param realname:
    :param username:
    :param password:
    :param email:
    :return:
    创建注册用户接口
    by:王健 at:2016-04-21
    """

    if code != request.session.get('smscode', 1234):
        return get_result(False, u'短信验证码输入错误，请核实！', None)
    if username != request.session.get('smsusername', ''):
        return get_result(False, u'发送验证码的手机号，和注册的手机号不符合。请重新输入', None)

    if get_user_model().objects.filter(username=username).exists():
        return get_result(False, u'手机号已经存在。请更换手机号', None)
    user = get_user_model()()
    user.username = username
    user.realname = realname
    user.set_password(password)
    user.email = email
    user.save()
    user.icon_url = getUserIconUrl(user.id, user.realname)
    user.save(update_fields=['icon_url'])
    request.session['smscode'] = None

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth_login(request, user)
    res = user.toJSON()
    sessionid = request.session.session_key
    if not sessionid:
        request.session.save()
        sessionid = request.session.session_key
    res['sessionid'] = sessionid
    return get_result(True, u'注册成功', res)


@check_request_parmes(username=("手机号", "r,phone"), password=(" password", "r"))
def login(request, username, password):
    """
    常规登录
    :param request:
    :param username:
    :param password:
    :return:
    常规登录 使用手机号 和 密码
    by:王健 at:2016-04-21
    """
    user = authenticate(username=username, password=password)
    if user is None:
        return get_result(False, u'账号或密码错误')
    if not user.is_active:
        return get_result(False, u'用户已经停止使用。', status_code=5)
    auth_login(request, user)
    res = user.toJSON()
    sessionid = request.session.session_key
    if not sessionid:
        request.session.save()
        sessionid = request.session.session_key
    res['sessionid'] = sessionid
    return get_result(True, u'登录成功', res)


@check_request_parmes(username=("手机号", "r,phone"), password=(" password", "r"))
def simple_login(request, username, password):
    """
    简单登录,只返回 sessionid
    :param request:
    :param username:
    :param password:
    :return:
    只返回sessionid的登录
    by:王健 at:2016-04-21
    """
    user = authenticate(username=username, password=password)
    if not user:
        return get_result(False, u'用户名密码错误')
    if not user.is_active:
        return get_result(False, u'用户已经停止使用。', status_code=5)
    auth_login(request, user)
    sessionid = request.session.session_key
    if not sessionid:
        request.session.save()
        sessionid = request.session.session_key
    return get_result(True, u'登录成功', {"sessionid": sessionid})


def sync_cookie(request):
    """
    同步cookie
    :param request:
    :return:
    同步cookie
    by:王健 at:2016-04-21
    """
    sessionid = request.session.session_key
    if not sessionid:
        request.session.save()
        sessionid = request.session.session_key
    return get_result(True, u'', {"sessionid": sessionid})


@check_request_parmes(username=("手机号", "r,phone"), newpassword=("新密码", "r"), code=("验证码", "r,int"))
def change_password_by_code(request, username, newpassword, code):
    """
    通手机验证码修改密码
    :param username:
    :param request:
    :param newpassword:
    :param code:
    :return:
    通手机验证码修改密码
    by:王健 at:2016-04-21
    """
    if code != request.session.get('smscode', 1234):
        return get_result(False, u'短信验证码输入错误，请核实！')
    if username != request.session.get('smsusername'):
        return get_result(False, u'手机号和短信验证码发送的手机号不一致，请核实！', None)
    try:
        user = get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        return get_result(False, u'用户不存在')
    if not user.is_active:
        return get_result(False, u'用户已经停止使用。')

    user.set_password(newpassword)
    user.save(update_fields=['password'])

    return get_result(True, u'重置密码成功,请重新登录')


@check_request_parmes(newpassword=("新密码", "r"), oldpassword=("新密码", "r"))
@client_login_required
def change_password(request, newpassword, oldpassword):
    """
    通过原密码修改新密码
    :param oldpassword:
    :param request:
    :param newpassword:
    :return:
    通过原密码修改新密码
    by:王健 at:2016-04-21
    """
    if not request.user.is_active:
        return get_result(False, u'用户已经停止使用。')
    if not request.user.check_password(oldpassword):
        return get_result(False, u'密码错误。')

    request.user.set_password(newpassword)
    request.user.save(update_fields=['password'])

    return get_result(True, u'重置密码成功', None)


@check_request_parmes(tel=("手机号", "r,phone"))
def send_sms_code_reg(request, tel):
    """
    注册发送验证码
    :param request:
    :param tel:
    :return:
    注册时发送验证码
    by:王健 at:2016-04-21
    """
    # todo:虚假发送验证码,待完善
    before_sms = request.session.get('smstime')
    if before_sms and time.time() - before_sms < 60:
        return get_result(False, u'每分钟只能发送一条验证码短信')
    num = request.session.get('smsnum', 0)
    if num > 10:
        return get_result(False, u'当天发送短信验证码太多')
    request.session['smsusername'] = tel
    request.session['smstime'] = time.time()
    request.session['smscode'] = 1234
    request.session['smsnum'] = num + 1

    return get_result(True, u'发送验证码成功')


@check_request_parmes(tel=("手机号", "r,phone"))
def send_sms_code(request, tel):
    """
    发送修改密码的验证码
    :param request:
    :param tel:
    :return:
    发送修改密码的验证码
    by:王健 at:2016-04-21
    """
    # todo:虚假发送验证码,待完善
    before_sms = request.session.get('smstime')
    if before_sms and time.time() - before_sms < 60:
        return get_result(False, u'每分钟只能发送一条验证码短信')
    num = request.session.get('smsnum', 0)
    if num > 10:
        return get_result(False, u'当天发送短信验证码太多')
    if get_user_model().objects.filter(username=tel).exists():
        request.session['smsusername'] = tel
        request.session['smstime'] = time.time()
        request.session['smscode'] = 1234
        request.session['smsnum'] = num + 1
    else:
        return get_result(False, u'手机号不存在')

    return get_result(True, u'发送验证码成功')


@client_login_required
def my_userinfo(request):
    """
    获取我的个人信息
    :param request:
    :return:
    获取我的个人信息
    by:王健 at:2016-04-21
    """
    user = request.user.toJSON()
    return get_result(True, u'', user)
