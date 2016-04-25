# coding=utf-8
# Date: 15/3/8
# Time: 14:58
# Email:fanjunwei003@163.com
import base64
import hashlib
import logging
import re
import threading
import traceback
import time
import urllib

import datetime
from django.conf import settings
from django.core.cache import cache
import phonenumbers
from raven import Client
import requests
# from wechat_sdk import WechatBasic
# from wechat_sdk.exceptions import OfficialAPIError
from util import demjson
from django.utils.http import urlencode

__author__ = u'范俊伟'
wechatObjLock = threading.RLock()
log = logging.getLogger('django')


class ErrorMessage(Exception):
    pass


def tel_segment(tel):
    """
    号码归属地查询
    :param tel:
    :return:
    """
    try:
        res = requests.get("http://virtual.paipai.com/extinfo/GetMobileProductInfo?mobile=%s&amount=10000" % tel,
                           timeout=20)
        if res.ok:
            text = res.text
            dre = re.compile(r'(\{.*\})', re.DOTALL)
            match = dre.search(text)
            if match:
                respCmtJson = match.groups()[0]
                res = demjson.decode(respCmtJson)
                return res.get('province'), res.get('cityname'), res.get('isp')
    except:
        common_except_log()
    return None, None, None


def getCachedAccessWechatObj(appID=None, appSecret=None, token=None):
    """
    获取微信对象
    by: 范俊伟 at:2015-04-21
    :param appID:
    :param appSecret:
    :param token:
    :return:
    """
    if not appID:
        appID = settings.WECHAT_APP_ID
    if not appSecret:
        appSecret = settings.WECHAT_APPSECRET
    if not token:
        token = settings.SERVER_TOKEN
    wechatObjLock.acquire()
    try:
        if not appID or not appSecret:
            return None
        access_token_info = cache.get('access_token_info_%s' % appID, None)
        if access_token_info:
            access_token = access_token_info.get('access_token')
            access_token_expires_at = access_token_info.get('access_token_expires_at')
        else:
            access_token = None
            access_token_expires_at = None
        # wechatObj = WechatBasic(token=token, appid=appID, appsecret=appSecret,
        #                         access_token=access_token,
        #                         access_token_expires_at=access_token_expires_at)
        # access_token_info = wechatObj.get_access_token()  # 检测access_token,更新access_token
        cache.set('access_token_info_%s' % appID, access_token_info)
        # return wechatObj
    except :
        common_except_log()
        return None
    finally:
        wechatObjLock.release()


def clearWechatTokenCache(appID=None):
    """
    清除微信token缓存
    by: 范俊伟 at:2015-04-21
    :param appID:
    :return:
    """
    if not appID:
        appID = settings.WECHAT_APP_ID
    cache.set('access_token_info_%s' % appID, None)



class ConcurrentModificationException(Exception):
    pass


def common_except_log():
    """
    通用错误输出
    by: 范俊伟 at:2015-03-08
    :return:
    """
    client = Client(settings.SENTRY_CLIENT_KEY)
    client.user_context({
        "error": traceback.format_exc(),
    })
    client.captureException()
    log.error('\n**common_except_log**\n' + traceback.format_exc())
    print '\n**common_except_log**\n' + traceback.format_exc()


def common_except_info(info, from_function):
    """
    输出特定消息到sentry中
    by: 马志  at: 2015-11-27

    """
    client = Client(settings.SENTRY_CLIENT_KEY)
    client.captureMessage("info:%s,from:%s" % (info, from_function))


def find_file_type(filename):
    """
    根据文件名找到文件类型
    by: 尚宗凯 at:2015-03-30
    改为根据最后一个确定扩展名
    by: 尚宗凯 at:2015-03-30
    :return:
    """
    if filename:
        a = filename.strip().split(".")
        if len(a) > 1:
            return a[-1]
    return ""


def getip(ethname):
    """
    获取ip地址
    by: 范俊伟 at:2015-08-03
    :param ethname:
    :return:
    """
    try:
        import socket
        import struct
        import fcntl

        if type(ethname) == unicode:
            ethname = ethname.encode('utf-8')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])
    except:
        return None


def query_to_list(query):
    """
    query转为列表
    by: 范俊伟 at:2015-07-08
    :param query:
    :return:
    """
    if query == None:
        return None
    result = []
    for i in query:
        result.append(i.toJSON())
    return result


def now_timeline():
    return int(time.time())


def convert_version(version):
    """
    根据字符串verson 转化成 数字
    by:王健 at:2015-09-08
    :param version:
    :return:
    """
    tmp = version.split('.')
    try:
        a, b, c = tmp[0], tmp[1], tmp[2]
    except Exception as e:
        print e
        return 0
    if int(b) < 10:
        b = "0" + b
    if int(c) < 10:
        c = "0" + c
    return a + b + c


def getUserIconUrl(id, name, width=None, height=None):
    from util.middleware import getHost
    if not name:
        return ""
    if type(name) == str:
        name = name.decode('utf-8')
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(name)
    to_len = min(len(name), 2)
    if match:
        name = name[len(name) - to_len:]
    else:
        name = name[:to_len]

    index = id % len(settings.USER_ICON_BG_COLORS)
    color = settings.USER_ICON_BG_COLORS[index]

    return "http://%s/sys/text_icon?%s" % (
            getHost(), urllib.urlencode({"color": color, "text": name, "width": width or '', "height": height or ''}))



def getPhoneNumber(number):
    x = phonenumbers.parse(number, 'CN')
    number = str(x.national_number)
    if len(number) != 11:
        raise Exception("手机号格式错误")
    return number


def get_request_query_string(request, new_params=None, remove=None):
    '''
    返回当前url的查询参数(query string)
    by:范俊伟 at:2015-01-21
    :param new_params:所要添加的新参数,以dic形式提供
    :param remove:所要去除的字段,以array形式提供
    '''
    if new_params is None:
        new_params = {}
    if remove is None:
        remove = []
    p = dict(request.GET.items()).copy()
    for r in remove:
        for k in p.keys():
            if k.startswith(r):
                del p[k]
    for k, v in new_params.items():
        if v is None:
            if k in p:
                del p[k]
        else:
            p[k] = v
    qs = urlencode(p)
    if qs:
        return '?%s' % qs
    else:
        return ''



def strMD5(string):
    """
    计算MD5
    by: 范俊伟 at:2015-04-21
    :param string:
    :return:
    """
    if type(string) == unicode:
        string = string.encode('utf-8')
    else:
        string = str(string)
    return hashlib.md5(string).hexdigest().upper()


class TtjdSignal(object):
    def __init__(self):
        self.recivers = []

    def connect(self, reciver, sender=None):
        for i in self.recivers:
            if i.get("reciver") == reciver and i.get('sender')==sender:
                return

        item = {}
        item['reciver'] = reciver
        item['sender'] = sender
        self.recivers.append(item)

    def send(self, sender=None, *args, **kwargs):
        responses = []
        for i in self.recivers:
            if not sender or sender == i.get("sender"):
                func = i.get('reciver')
                kwargs['sender'] = sender
                responses.append([func, func(**kwargs)])
        return responses


def date_to_datetime(dates):
    """
    date类型转datetime
    by: 魏璐 at:2016-03-21
    :param dates:
    :return:
    """
    return datetime.datetime(year=dates.year, month=dates.month, day=dates.day, hour=0, minute=0, second=0)


def request_to_dict(request):
    result = {}
    items = request.items()
    for i in items:
        result[i[0]] = i[1]
    return result
