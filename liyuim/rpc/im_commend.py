#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/29 下午9:41
# file: im_commend.py
# Email: wangjian2254@icloud.com
# Author: 王健
import json

from django.conf import settings
from grpc.beta import implementations
import liyuim_pb2

_TIMEOUT_SECONDS = 10

channel = None
stub = None

try:
    channel = implementations.insecure_channel(settings.MQTT_HOST, settings.MQTT_PORT)
    stub = liyuim_pb2.beta_create_MqttCommend_stub(channel)
except:
    pass


def init():
    global channel
    global stub

    channel = implementations.insecure_channel(settings.MQTT_HOST, settings.MQTT_PORT)
    stub = liyuim_pb2.beta_create_MqttCommend_stub(channel)


def mqtt_commend(route, parms, is_sync=True):

    commend = {'route': route, 'parms': parms}
    if is_sync:
        response = stub.CommendIm(liyuim_pb2.IMRequest(commend=json.dumps(commend)), _TIMEOUT_SECONDS)

        result = json.loads(response.result)

        return result
    else:
        feature = stub.CommendIm.future(liyuim_pb2.IMRequest(commend=json.dumps(commend)))

        return

