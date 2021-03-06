#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/23 下午8:11
# file: models_doc.py
# Email: wangjian2254@icloud.com
# Author: 王健

import datetime

import mongoengine
from django.conf import settings

if settings.NEED_MONGODB_HOST:
    try:
        mongoengine.connect(
            host=settings.NEED_MONGODB_HOST,
        )
    except:
        pass


class ChatSession(mongoengine.Document):
    """
    会话
    by:王健 at:2016-04-23
    """
    session_id = mongoengine.StringField(max_length=64, primary_key=True, verbose_name="会话id")
    owner = mongoengine.IntField(verbose_name="回话隶属的用户")
    target = mongoengine.IntField(verbose_name="聊天对象")
    target_type = mongoengine.IntField(verbose_name="聊天对象类型", help_text="0:用户;1:群;2:系统")
    is_top = mongoengine.BooleanField(default=False, verbose_name="是否置顶")
    nickname = mongoengine.StringField(max_length=30, verbose_name="聊天对象昵称")
    content = mongoengine.StringField(max_length=2000, verbose_name="消息")
    update_time = mongoengine.DateTimeField()
    time = mongoengine.IntField(verbose_name="已读时间戳")

    meta = {
        'indexes': ['owner', 'target', 'target_type', 'is_top', 'update_time']
    }


class MessageUserRead(mongoengine.Document):
    """
    消息已读未读
    by:王健 at:2016-04-25
    """
    message_id = mongoengine.StringField(max_length=64, verbose_name="消息id")
    user = mongoengine.IntField(verbose_name="消息接收人")
    is_read = mongoengine.BooleanField(verbose_name="是否已读")


class ChatMessage(mongoengine.Document):
    """
    接口请求计数表
    by: 范俊伟 at:2015-04-16
    """
    message_id = mongoengine.StringField(max_length=64, primary_key=True, verbose_name="消息id")
    fuser = mongoengine.IntField(verbose_name="消息发送方")
    fnick = mongoengine.StringField(max_length=30, verbose_name="发送方昵称")
    fclient_id = mongoengine.StringField(max_length=50, verbose_name="发送方clientid")
    fdevice_id = mongoengine.StringField(max_length=50, verbose_name="发送方设备id")
    target = mongoengine.IntField(verbose_name="接收方")
    target_type = mongoengine.IntField(verbose_name="聊天对象类型", help_text="0:用户;1:群;2:系统")
    time = mongoengine.IntField(verbose_name="时间戳")
    ctype = mongoengine.IntField(default=0, verbose_name="消息类型")
    is_read = mongoengine.BooleanField(default=False, verbose_name="已读")
    readuserlist = mongoengine.ListField(mongoengine.ReferenceField(MessageUserRead))

    content = mongoengine.StringField(max_length=2000, verbose_name="消息")
    ext = mongoengine.StringField(max_length=4000, verbose_name="扩展属性")

    id_client = mongoengine.StringField(max_length=50, verbose_name="客户端生成的id,用于判断消息发送是否成功")
    push_content = mongoengine.StringField(max_length=50, verbose_name="推送显示的内容")
    push_payload = mongoengine.StringField(max_length=500, verbose_name="推送属性")
    is_push = mongoengine.BooleanField(default=True, verbose_name="是否需要推送")
    is_unreadable = mongoengine.BooleanField(default=True, verbose_name="是否需要计入未读")

    meta = {
        'indexes': ['fuser', 'target', 'target_type', 'time', 'readuserlist', 'ctype', 'is_read', 'is_unreadable']
    }
