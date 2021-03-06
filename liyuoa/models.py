# coding=utf-8
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from util.basemodel import BaseModel, ValuesQuerySet, JSONBaseMixin, ModefyMixin


class LYUser(AbstractUser, JSONBaseMixin, ModefyMixin):
    """
    基础用户类
    by:王健 at:2016-04-18
    username 字段 保存的是用户的手机号
    by:王健 at:2016-04-21
    """
    icon_url = models.URLField(verbose_name=u'图标url', null=True)
    realname = models.CharField(max_length=8, verbose_name=u'真实姓名', help_text=u'真实姓名')
    imusername = models.CharField(max_length=50, unique=True, null=True, verbose_name=u'即时通信账号', help_text=u'即时通信账号')
    impassword = models.CharField(max_length=50, null=True, verbose_name=u'即时通信账号密码', help_text=u'即时通信账号密码')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = ValuesQuerySet.as_manager()

    class Meta:
        list_json = ['realname', 'icon_url', 'id']
        detail_json = ['username', 'imusername', 'impassword', 'email', 'username', 'is_active', 'is_staff', 'date_joined']

    def __unicode__(self):
        return u'$s#%s' % (self.pk, self.realname)

    def save(self, **kwargs):
        if not self.imusername:
            self.imusername = str(uuid.uuid4())
        if not self.impassword:
            self.impassword = str(uuid.uuid4())
        super(LYUser, self).save(**kwargs)
        self.clean_old()


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
    namespace = models.CharField(max_length=20, db_index=True, blank=True, verbose_name=u'模块名')

    class Meta:
        list_json = ['flag', 'name', 'id', 'type_flag']
        detail_json = ['create_time', 'is_show', 'is_active', 'desc', 'namespace']


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


class AppApi(BaseModel):
    """
    应用接口
    by:王健 at:2016-04-20
    """
    name = models.CharField(max_length=50, db_index=True, verbose_name=u'接口名称')
    app = models.ForeignKey(AppInfo, verbose_name=u'应用', null=True)
    url = models.CharField(max_length=100, unique=True, verbose_name=u'绝对url')
    namespace = models.CharField(max_length=150, db_index=True, verbose_name=u'函数目录')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    code_content = models.TextField(verbose_name=u'代码')
    response_type = models.CharField(max_length=10, default='', blank=True, verbose_name=u'返回值类型')

    class Meta:
        list_json = ['name', 'url', 'id', 'namespace', 'update_time']
        detail_json = ['create_time', 'is_active', 'code_content', 'response_type']


class AppApiCareUser(BaseModel):
    """
    接口关心开发者, 接口发生变动后通知相关人员
    by:王健 at:2016-04-20
    """
    api = models.ForeignKey(AppApi, verbose_name=u'隶属api')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'用户')
    is_confirm = models.BooleanField(default=False, verbose_name=u'是否处理过')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

    class Meta:
        list_json = ['user_id', 'user__icon_url', 'id', 'user__realname', 'update_time', 'api_id', 'is_confirm']
        detail_json = ['create_time', 'is_active']


class AppApiParameter(BaseModel):
    """
    接口参数
    by:王健 at:2016-04-20
    """
    api = models.ForeignKey(AppApi, verbose_name=u'隶属api')
    name = models.CharField(max_length=30, db_index=True, verbose_name=u'参数名')
    title = models.CharField(max_length=20, verbose_name=u'参数中文名')
    desc = models.CharField(max_length=100, verbose_name=u'参数备注')
    default = models.CharField(max_length=30, null=True, verbose_name=u'参数默认值')
    parm_type = models.CharField(max_length=10, verbose_name=u'参数类型')
    is_required = models.BooleanField(default=False, verbose_name=u'是否必须')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

    class Meta:
        list_json = ['name', 'title', 'id', 'parm_type', 'is_required', 'update_time', 'api_id', 'desc', 'default']
        detail_json = ['create_time', 'is_active']


class AppApiResponse(BaseModel):
    """
    接口参数
    by:王健 at:2016-04-20
    """
    api = models.ForeignKey(AppApi, verbose_name=u'隶属api')
    name = models.CharField(max_length=30, db_index=True, verbose_name=u'字段名')
    title = models.CharField(max_length=20, verbose_name=u'字段中文名')
    desc = models.CharField(max_length=100, verbose_name=u'字段备注')
    value_type = models.CharField(max_length=10, verbose_name=u'数值类型')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

    class Meta:
        list_json = ['name', 'title', 'id', 'value_type', 'update_time', 'api_id', 'desc']
        detail_json = ['create_time', 'is_active']


class AppApiComment(BaseModel):
    """
    接口修改 或 对接口的评论
    by:王健 at:2016-04-20
    """
    api = models.ForeignKey(AppApi, verbose_name=u'隶属api')
    content = models.TextField(verbose_name=u'修改内容,或评论内容')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=u'隶属用户')
    username = models.CharField(max_length=30, verbose_name=u'匿名昵称')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='api_to_comment', verbose_name=u'隶属用户')
    to_comment = models.ForeignKey('AppApiComment', null=True, verbose_name=u'父级评论')
    source = models.IntegerField(default=0, verbose_name=u'0:修改注释;1:文档自动对比;2:人工评论')
    attachments = models.ManyToManyField('nsbcs.NsFile', verbose_name=u'附件')

    class Meta:
        list_json = ['content', 'user_id', 'id', 'api_id', 'user__realname', 'user__icon_url', 'to_user__realname',
                     'to_user__icon_url', 'create_time', 'to_comment_id', 'to_comment__content', 'to_comment__user_id',
                     'to_comment__user__icon_url', 'to_comment__user__realname', 'source', 'username']
        detail_json = ['is_active']


class UserHeadIcon(BaseModel):
    """
    即时通信发送的文件
    by:王健 at:2016-04-23
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'上传者')
    nsfile = models.ForeignKey('nsbcs.NsFile', verbose_name=u'附件')

    def save(self, **kwargs):
        super(UserHeadIcon, self).save(**kwargs)
        self.nsfile.update_file_status()

    class Meta:
        list_json = ['id', 'user_id', 'nsfile_id', 'nsfile__name', 'nsfile__filetype', 'nsfile__size',
                     'nsfile__fileurl', 'nsfile__bucket']
        detail_json = ['create_time', 'is_active']
