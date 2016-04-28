#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/28 上午11:52
# file: views_qrcode.py
# Email: wangjian2254@icloud.com
# Author: 王健
from urllib import urlencode

from util.jsonresult import get_result
from util.loginrequired import check_request_parmes, check_response_results
from util.middleware import getHost


@check_request_parmes(org_id=("组织id", "r,int"))
@check_response_results(text=("二维码数值", ""))
def qrcode_join_org_string(request, org_id):
    """
    生成登录二维码数值
    :param request:
    :return:
    生成登录的二维码数值
    by:王健 at:2016-04-21
    """
    args = ['3', str(org_id)]
    p = '|'.join(args)
    parms = {"p": p}
    text = "http://%s/sys/qrcode2?%s" % (getHost(), urlencode(parms))
    return get_result(True, '', {"text": text})
