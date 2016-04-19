# coding=utf-8
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from util.basemodel import BaseModel, ValuesQuerySet


class LYUser(AbstractUser):
    """
    基础用户类
    by:王健 at:2016-04-18
    """
    tel = models.CharField(max_length=20, unique=True, verbose_name=u'手机号', null=True, blank=False)
    icon_url = models.URLField(verbose_name=u'图标url', null=True)
    realname = models.CharField(max_length=8, null=True, blank=True, verbose_name=u'真实姓名', help_text=u'真实姓名')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = ValuesQuerySet.as_manager()

    class Meta:
        list_json = ['realname', 'icon_url', 'id']
        detail_json = ['username', 'email', 'tel', 'is_active', 'is_staff', 'date_joined']

    def __unicode__(self):
        return unicode(self.name)


class AppInfo(BaseModel):
    """
    应用信息
    by:王健 at:2015-10-09
    """
    flag = models.CharField(max_length=50, unique=True, null=True, verbose_name=u'功能标记')
    name = models.CharField(max_length=20, verbose_name=u"应用名称")
    type_flag = models.CharField(max_length=20, verbose_name=u'应用类型')
    is_show = models.BooleanField(default=True, verbose_name=u'是否显示在应用列表')
    desc = models.TextField(blank=True, verbose_name=u'应用描述')
    namespace = models.CharField(max_length=20, db_index=True, blank=True, verbose_name=u'应用描述')

    class Meta:
        list_json = ['flag', 'name', 'id', 'type_flag']
        detail_json = ['create_time', 'is_active', 'desc']


class AppRole(BaseModel):
    """
    应用内角色信息
    by:王健 at:2015-10-09
    """
    role = models.CharField(max_length=20, verbose_name=u'角色')
    name = models.CharField(max_length=20, verbose_name=u"角色名称")
    desc = models.TextField(blank=True, verbose_name=u'应用描述')
    app = models.ForeignKey(AppInfo)

    class Meta:
        unique_together = (("role", "app"),)
        list_json = ['role', 'name', 'id', 'desc']
        detail_json = ['create_time', 'is_active']

