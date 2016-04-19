# coding=utf-8
# Date: 15/3/31
# Time: 10:33
# Email:fanjunwei003@163.com
from needserver.models import NSUser
from ns_manage.models import ClientUser
from util.emoji import replace_emoji
from util.tools import common_except_log

__author__ = u'范俊伟'


class UserIdAuthBackend:
    """
    二维码用户登录授权
    by: 范俊伟 at:2016-02-09
    """

    def authenticate(self, user_id=None):
        try:
            user = NSUser.objects.get(id=user_id)
            return user
        except NSUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = NSUser.objects.get(id=user_id)
            return user
        except NSUser.DoesNotExist:
            return None


class OpenidAuthBackend:
    """
    微信用户授权
    by: 范俊伟 at:2015-04-30
    """

    def authenticate(self, openid=None, userinfo=None):
        try:
            clientUser = ClientUser.objects.get(openid=openid)
        except ClientUser.DoesNotExist:
            clientUser = ClientUser()
            clientUser.openid = openid
            clientUser.user_type = 1
            clientUser.save()
        try:
            if userinfo:
                clientUser.name = replace_emoji(userinfo.get('nickname', None))
                clientUser.sex = userinfo.get('sex', None)
                clientUser.language = userinfo.get('language', None)
                clientUser.city = userinfo.get('city', None)
                clientUser.province = userinfo.get('province', None)
                clientUser.country = userinfo.get('country', None)
                clientUser.icon_url = userinfo.get('headimgurl', None)
                clientUser.subscribe_time = userinfo.get('subscribe_time', None)
            clientUser.save()
        except:
            common_except_log()
        return clientUser

    def get_user(self, user_id):
        try:
            user = ClientUser.objects.get(id=user_id)
            return user
        except ClientUser.DoesNotExist:
            return None
