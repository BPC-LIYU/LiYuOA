#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/23 下午13:38
# file: models.py
# Email: wangjian2254@icloud.com
# Author: 王健

from django.conf import settings
from django.db import models

# Create your models here.
from util.basemodel import BaseModel


class FriendGroup(BaseModel):
    """
    好友分组
    by:王健 at:2016-04-23
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'隶属用户')
    name = models.CharField(max_length=20, verbose_name=u'分组名称')
    parent = models.ForeignKey('FriendGroup', null=True, verbose_name=u'隶属分组')

    class Meta:
        list_json = ['user_id', 'name', 'id', 'parent_id']
        detail_json = ['create_time', 'is_active']


class Friend(BaseModel):
    """
    好友关系
    by:王健 at:2016-04-23
    """
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'好友')
    nickname = models.CharField(max_length=30, verbose_name=u'好友备注名')
    group = models.ForeignKey(FriendGroup, verbose_name=u'分组', null=True, help_text=u'没分组的就是"我的好友"分组,默认')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendowner', null=True, verbose_name=u'好友')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    is_black = models.BooleanField(default=False, verbose_name=u'是否黑名单')
    is_muted = models.BooleanField(default=False, verbose_name=u'是否静音')

    class Meta:
        unique_together = (('friend', 'owner'),)
        list_json = ['friend_id', 'friend__realname', 'friend__icon_url', 'nickname', 'id', 'owner_id',
                     'group_id', 'update_time', 'is_black']
        detail_json = ['create_time', 'is_active']


class FriendApply(BaseModel):
    """
    好友申请
    by:王健 at:2016-04-23
    """
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'收到申请的用户')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendapplyowner', verbose_name=u'发出申请的用户')
    status = models.IntegerField(default=0, db_index=True, verbose_name=u'状态', help_text=u'0:未处理,1:同意')
    content = models.CharField(max_length=50, verbose_name=u'申请信息')

    class Meta:
        list_json = ['user_id', 'owner__realname', 'owner__icon_url', 'id', 'owner_id',
                     'content', 'create_time']
        detail_json = ['is_active']


class TalkGroup(BaseModel):
    """
    用户创建的讨论组
    by:王健 at:2016-04-23
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'群主')
    name = models.CharField(max_length=30, verbose_name=u'群名称')
    max_member_count = models.IntegerField(default=100, verbose_name=u'成员数限制')
    group_type = models.IntegerField(default=0, verbose_name=u'群类型', help_text=u'0:普通群;1:企业群;2:企业部门;3:讨论组')
    is_add = models.BooleanField(default=True, verbose_name=u'成员是否可自由加人')
    flag = models.CharField(max_length=50, db_index=True, verbose_name=u'群成员md5')
    icon_url = models.CharField(max_length=255, null=True, verbose_name=u'群头像')

    class Meta:
        list_json = ['owner_id', 'owner__realname', 'owner__icon_url', 'name', 'id', 'max_member_count', 'group_type',
                     'icon_url', 'is_add']
        detail_json = ['create_time', 'is_active']


class TalkUser(BaseModel):
    """
    群成员
    by:王健 at:2016-04-23
    """
    talkgroup = models.ForeignKey(TalkGroup, verbose_name=u'群')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'群成员')
    nickname = models.CharField(max_length=30, verbose_name=u'群名片')
    role = models.IntegerField(default=0, verbose_name=u'群角色', help_text=u'0:成员;1:管理员;')
    read_timeline = models.IntegerField(default=0, verbose_name=u'已读时间戳')
    is_muted = models.BooleanField(default=False, verbose_name=u'是否静音')

    class Meta:
        list_json = ['id', 'talkgroup_id', 'user__realname', 'user__icon_url', 'nickname', 'role', 'is_muted', 'read_timeline']
        detail_json = ['create_time', 'is_active']


class TalkGongGao(BaseModel):
    """
    群公告
    by:王健 at:2016-04-23
    """
    talk = models.ForeignKey(TalkGroup, verbose_name=u'群')
    tuser = models.ForeignKey(TalkUser, verbose_name=u'发布人')
    content = models.TextField(verbose_name=u'公告内容')

    class Meta:
        list_json = ['id', 'talk_id', 'tuser__nickname', 'tuser__user__icon_url', 'content']
        detail_json = ['create_time', 'is_active']


class TalkApply(BaseModel):
    """
    群申请
    by:王健 at:2016-04-23
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'申请发出人')
    talkgroup = models.ForeignKey(TalkGroup, verbose_name=u'申请群')
    status = models.IntegerField(default=0, db_index=True, verbose_name=u'状态', help_text=u'0:未处理,1:同意,2:拒绝')
    content = models.CharField(max_length=50, verbose_name=u'申请信息')
    reply = models.CharField(max_length=50, verbose_name=u'处理信息')
    checker = models.ForeignKey(TalkUser, null=True, verbose_name=u'处理人')

    class Meta:
        list_json = ['id', 'talkgroup_id', 'talkgroup__icon_url', 'talkgroup__name', 'status', 'content', 'reply', 'checker_id',
                     'checker__nickname', 'checker__user__icon_url']
        detail_json = ['create_time', 'is_active']


class IMFile(BaseModel):
    """
    即时通信发送的文件
    by:王健 at:2016-04-23
    """
    owner = models.ForeignKey(TalkUser, verbose_name=u'发送者')
    chat_id = models.IntegerField(db_index=True, verbose_name=u'发送目标')
    is_group = models.BooleanField(default=False, db_index=True, verbose_name=u'是否发给群')
    file_type = models.CharField(max_length=10, db_index=True, verbose_name=u'附件类型')
    file = models.ForeignKey('nsbcs.NsFile', verbose_name=u'附件')

    class Meta:
        list_json = ['id', 'chat_id', 'is_group', 'file_type', 'file_id', 'file__name', 'file__filetype', 'file__size']
        detail_json = ['create_time', 'is_active']
