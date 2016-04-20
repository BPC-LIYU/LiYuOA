# coding=utf-8
# Date: 15/3/4
# Time: 14:09
# Email:fanjunwei003@163.com
import hashlib
import logging

from django import http
from django.conf import settings
import pickle
import time

from liyuoa.models import LYUser
from util.tools import common_except_log
from django.contrib import auth
from django.utils.functional import SimpleLazyObject
from threading import local

__author__ = u'范俊伟'


class UserAgentMiddleware(object):
    """
    UserAgent中间件
    by: 范俊伟 at:2015-03-04
    """

    def process_request(self, request):
        """
        页面请求
        browserGroup: 设备大分类,smart_phone:智能机 feature_phone:功能机 空字串:pc或其他
        browserType: 设备类型,iphone,ipad,android,wp(windows phone),blackberry(黑莓),nokia(分智能机和功能机),空字串为pc或其他
        by: 范俊伟 at:2015-03-04
        :param request:
        :return:
        """
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        if not user_agent.find('iphone') == -1:
            request.browserType = 'iphone'
            request.browserGroup = 'smart_phone'
        elif not user_agent.find('ipad') == -1:
            request.browserType = 'ipad'
            request.browserGroup = 'smart_phone'
        elif not user_agent.find('android') == -1:
            request.browserType = 'android'
            request.browserGroup = 'smart_phone'
        elif not user_agent.find('windows phone') == -1:
            request.browserType = 'wp'
            request.browserGroup = 'smart_phone'
        elif not user_agent.find('blackberry') == -1:
            request.browserType = 'blackberry'
            if not user_agent.find('applewebkit') == -1:
                request.browserGroup = 'smart_phone'
            if not user_agent.find('opera') == -1:
                request.browserGroup = 'smart_phone'
            else:
                request.browserGroup = 'feature_phone'
        elif (not user_agent.find('symbian') == -1):
            request.browserType = 'nokia'
            if not user_agent.find('applewebkit') == -1:
                request.browserGroup = 'smart_phone'
            else:
                request.browserGroup = 'feature_phone'
        else:
            request.browserType = ''
            request.browserGroup = ''

        if user_agent.find('micromessenger') != -1:
            request.isWechat = True
        else:
            request.isWechat = False


class SessionTransferMiddleware(object):
    """
    session传递
    by: 范俊伟 at:2015-07-02
    """

    def process_request(self, request):
        session_key = request.REQUEST.get('sessionid', None)
        if not session_key:
            session_key = request.META.get('HTTP_SESSIONID', None)
        request.url_cookie = session_key
        if session_key:
            try:
                request.COOKIES[settings.SESSION_COOKIE_NAME] = session_key
            except:
                common_except_log()

    def process_response(self, request, response):
        if request.url_cookie:
            sessionid = request.url_cookie
            response.set_cookie(settings.SESSION_COOKIE_NAME, sessionid)
        else:
            sessionid = request.session.session_key
            if not sessionid:
                request.session.save()
                sessionid = request.session.session_key
        response['sessionid'] = sessionid
        return response


def get_user(request):
    """
    摘取自django的AuthenticationMiddleware 中间件
    :param request:
    :return:
    """
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


class CustomAuthenticationMiddleware(object):
    def process_request(self, request):
        """
        request的预处理
        by:王健 at:2015-08-24
        :param request:
        :return:
        """
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        user_pickle = request.session.get('user_pickle', None)
        user_pickle_timeline = request.session.get('user_pickle_timeline', 0)
        if user_pickle and int(time.time()) - user_pickle_timeline < 5 * 60:
            request.user = pickle.loads(str(user_pickle))
        else:
            if user_pickle_timeline:
                del request.session['user_pickle_timeline']
            request.user = get_user(request)

    def process_response(self, request, response):
        """
        response的后处理
        by:王健 at:2015-08-24
        只序列化NSUser实例
        by: 范俊伟 at:2015-08-26
        判断user是否存在
        by: 范俊伟 at:2015-08-26
        :param request:
        :param response:
        :return:
        """
        if hasattr(request, 'user') and isinstance(request.user, LYUser):
            user_pickle_timeline = request.session.get('user_pickle_timeline', 0)
            if not user_pickle_timeline:
                try:
                    request.session['user_pickle'] = pickle.dumps(request.user)
                    request.session['user_pickle_timeline'] = int(time.time())
                except:
                    pass
        return response


current_request = local()


def getHost():
    """
    获取当前host
    :return:
    """
    if hasattr(current_request, 'request'):
        return current_request.request.META.get('HTTP_HOST', settings.HOST_URL)
    else:
        return settings.HOST_URL


class GlobRequestMiddleware(object):
    """
    存储当前request中间件
    by: 范俊伟 at:2015-10-15
    """

    def process_request(self, request):
        current_request.request = request


class ETagMiddleware(object):
    def process_response(self, request, response):
        use_etags = True

        if hasattr(request, 'use_etags'):
            use_etags = request.use_etags

        if use_etags:
            if response.has_header('ETag'):
                etag = response['ETag']
            elif response.streaming:
                etag = None
            else:
                etag = '"%s"' % hashlib.md5(response.content).hexdigest()
            if etag is not None:
                if (200 <= response.status_code < 300
                    and request.META.get('HTTP_IF_NONE_MATCH', '').replace(';gzip', '') == etag):
                    cookies = response.cookies
                    response = http.HttpResponseNotModified()
                    response.cookies = cookies
                else:
                    response['ETag'] = etag

        return response


class XIFrame(object):
    def process_response(self, request, response):
        response['X-Frame-Options'] = "ALLOW-FROM *"
        return response


class CorsMiddleware(object):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Headers'] = "sessionid"
        return response
