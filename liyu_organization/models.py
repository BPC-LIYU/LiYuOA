# coding=utf-8
from django.conf import settings
from django.db import models

# Create your models here.
from util.basemodel import BaseModel


class Organization(BaseModel):
    """
    组织表
    by:王健 at:2016-04-18
    """
    name = models.CharField(max_length=30, verbose_name=u'名称')
    icon_url = models.URLField(verbose_name=u'图标url', null=True)

    class Meta:
        list_json = ['name', 'icon_url', 'id']
        detail_json = ['create_time', 'is_active']


class Person(BaseModel):
    """
    组织和用户的关联表
    by:王健 at:2016-04-18
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    org = models.ForeignKey(Organization, verbose_name=u"隶属组织")
    realname = models.CharField(max_length=8, verbose_name=u'真实姓名')
    email = models.EmailField(null=True, verbose_name=u'电子邮件')
    title = models.CharField(max_length=10, verbose_name=u'职务')
    manage_type = models.IntegerField(db_index=True, default=0, verbose_name=u'身份类型',
                                      help_text=u"0:普通用户;1普通管理员2:超级管理员;")
    is_gaoguan = models.BooleanField(default=False, verbose_name=u'高管模式')
    is_show_tel = models.BooleanField(default=True, verbose_name=u'是否显示手机号')
    is_show_email = models.BooleanField(default=True, verbose_name=u'是否显示电子邮箱')

    class Meta:
        list_json = ['realname', 'user__icon_url', 'id', 'user_id', 'org_id', 'title', 'manage_type', 'is_active']
        detail_json = ['user__realname', 'create_time', 'user__imusername', 'is_gaoguan', 'is_show_tel', 'is_show_email']

    def __unicode__(self):
        return u'$s#%s' % (self.pk, self.realname)


class Group(BaseModel):
    """
    分组
    by:王健 at:2016-04-18
    """
    org = models.ForeignKey(Organization, verbose_name=u"隶属组织")
    name = models.CharField(max_length=30, verbose_name=u'分组名称')
    icon_url = models.URLField(verbose_name=u'图标url', null=True)
    members = models.ForeignKey(Person, verbose_name=u'分组成员')
    charge = models.ForeignKey(Person, related_name='group_charge', verbose_name=u'负责人', null=True)
    aide = models.ForeignKey(Person, related_name='group_aide', verbose_name=u'助手', null=True)
    sort = models.IntegerField(default=0, db_index=True, null=True, verbose_name=u'排序字段')
    parent = models.ForeignKey('Group', null=True, verbose_name=u'隶属关系')

    class Meta:
        list_json = ['name', 'icon_url', 'id', 'org_id', 'is_active', 'sort', 'parent_id']
        detail_json = ['org__name', 'create_time', 'charge_id', 'charge__user_id', 'charge__realname',
                       'charge__user__icon_url', 'aide__realname', 'aide__user__icon_url', 'aide_id', 'aide__user_id']


class OrgApply(BaseModel):
    """
    组织加入申请
    by:王健 at:2016-04-18
    """
    org = models.ForeignKey(Organization, verbose_name=u"隶属组织")
    checker = models.ForeignKey(Person, related_name='checker', null=True, blank=True,
                                verbose_name=u'审核人', help_text=u'隶属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    content = models.CharField(max_length=100, verbose_name=u'申请')
    status = models.IntegerField(default=0, db_index=True, verbose_name=u'状态', help_text=u'0:未处理,1:同意,2:拒绝')

    class Meta:
        list_json = ['user__realname', 'user__icon_url', 'id', 'org_id', 'status', 'content']
        detail_json = ['org__name', 'create_time', 'is_active', 'checker_id', 'checker__user_id',
                       'checker__user__icon_url', 'checker__realname']


class OrgApp(BaseModel):
    """
    组织中使用项目的关联表
    by:王健 at:2016-04-18
    """
    org = models.ForeignKey(Organization, verbose_name=u"隶属组织")
    app = models.ForeignKey('liyuoa.AppInfo', verbose_name=u'应用')
    sort = models.IntegerField(default=0, db_index=True, null=True, verbose_name=u'排序字段')

    class Meta:
        list_json = ['org_id', 'app__name', 'id', 'sort', 'app__flag', 'app__typeflag']
        detail_json = ['create_time', 'is_active']


class Permissions(BaseModel):
    """
    权限
    by:王健 at:2016-04-18
    """
    org = models.ForeignKey(Organization, verbose_name=u"隶属组织")
    person = models.ForeignKey(Person, verbose_name=u'用户')
    app = models.ForeignKey('liyuoa.AppInfo', verbose_name=u'应用')
    role = models.ForeignKey('liyuoa.AppRole', verbose_name=u'应用')

    class Meta:
        unique_together = (("org", "person", "app"),)

        list_json = ['org_id', 'app__name', 'app__flag', 'app__typeflag', 'id', 'role__name', 'role_id']
        detail_json = ['create_time', 'is_active', 'person_id', 'person__user_id', 'person__realname',
                       'person__user__icon_url', 'role__role', 'role__desc']

    def __unicode__(self):
        return u'$s#%s#%s' % (self.pk, self.app.name, self.role.name)
