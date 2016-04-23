# coding=utf-8
# Date: 11-12-8
# Time: 下午10:28
import collections
import json

import datetime

from django.core.paginator import Page
from django.http import HttpResponse

__author__ = u'王健'


BASE_DATE_FROMATE = '%Y-%m-%d'
BASE_DATETIME_FROMATE = '%Y-%m-%d %H:%M:%S'
BASE_TIME_FORMATE = '%H:%M'


class LiYuEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime(BASE_DATETIME_FROMATE)
        elif isinstance(obj, datetime.date):
            return obj.strftime(BASE_DATE_FROMATE)
        elif isinstance(obj, datetime.time):
            return obj.strftime(BASE_TIME_FORMATE)
        elif isinstance(obj, Page):
            return {"list": [x for x in obj.object_list], "page_index": obj.number, "page_count": obj.paginator.num_pages}
        return json.JSONEncoder.default(self, obj)


class JSONHttpResponse(HttpResponse):
    """
    继承HttpResponse类
    by:王健 at:2015-08-24
    """

    def __init__(self, json_data=None, *args, **kwargs):
        super(JSONHttpResponse, self).__init__(*args, **kwargs)
        self.json = json_data
        self.is_response_suggest = True


def is_success_mongodb_result(result):
    """
    根据mongo的返回信息，判断本次是否成功
    by:王健 at:2015-1-3
    :param result:
    :return:
    """
    if hasattr(result, 'err') and result['err'] is not None:
        return False
    else:
        return True


def get_result(success, message, result=None, status_code=0, dialog=0):
    """
    0 正常返回 code
    1 登录过期，需要重新登录
    2 组织id错误
    3 需要提供用户名和密码
    4 error
    5 用户禁止使用
    6 用户离开了当前组织
    7 组织余额不足，需要充值后继续使用
    8 权限不足
    9 手机号校验

    dialog 客户端提示类型
    0： 红字 3秒 提示
    1：Alert 提示
    by:王健 at:2015-1-3
    返回值，加上content-type = json
    :param success:
    :param message:
    :param result:
    :param status_code:
    :param dialog:
    :return:
    """

    data = {'success': success, 'message': message, 'status_code': status_code, 'dialog': dialog, 'result': result}
    if not success and status_code == 0:
        data['status_code'] = 4

    jsonstr = json.dumps(data, cls=LiYuEncoder)
    return JSONHttpResponse(content=jsonstr, json_data=data, content_type=u'application/json')


