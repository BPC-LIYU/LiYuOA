# coding=utf-8
# Date: 15/1/29'
# Email: wangjian2254@icloud.com

import django.db.models.options as options
from django.db import models

from util.model_tools import page_obj_query

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('list_json', 'detail_json')

__author__ = u'王健'


class ValuesQuerySet(models.QuerySet):

    def get_by_natural_key(self, username):
        """
        复制子 BaseUserManager 类
        :param username:
        :return:
        """
        return self.get(**{self.model.USERNAME_FIELD: username})

    def list_json(self, ex_parms=None, un_parms=None):
        """
        列表values Query_Set 返回
        by:王健 at:2016-04-19
        :param ex_parms:
        :param un_parms:
        :return:
        """
        if ex_parms is None:
            ex_parms = []

        ex_parms.extend(self.model._meta.list_json)
        ex_parms = set(ex_parms)
        if un_parms is not None:
            for k in un_parms:
                ex_parms.remove(k)
        ex_parms = list(ex_parms)
        ex_parms.sort()
        return self.values(*ex_parms)

    def detail_json(self, ex_parms=None, un_parms=None):
        """
        详情values Query_Set 返回
        by:王健 at:2016-04-19
        :param ex_parms:
        :param un_parms:
        :return:
        """
        if ex_parms is None:
            ex_parms = []
        ex_parms.extend(self.model._meta.detail_json)
        return self.list_json(ex_parms, un_parms)

    def get_serializer(self, **kwargs):
        """
        序列化 obj
        by:王健 at:2016-04-19
        :return:
        """
        try:
            return self.detail_json().filter(**kwargs)[0]
        except IndexError:
            raise self.model.DoesNotExist()

    def get_or_create_serializer(self, **kwargs):
        """
        封装get_or_create
        :param kwargs:
        :return:
        """
        obj, created = self.get_or_create(**kwargs)
        obj = self.detail_json().filter(pk=obj.pk)[0]
        return obj, created

    def get_page(self, page_index, page_size):
        """
        直接对 query_set进行分页
        by:王健 at:2016-04-19
        :param page_index:
        :param page_size:
        :return:
        """
        return page_obj_query(self, page_index, page_size)


class JSONBaseMixin(object):
    """
    obj 转 JSON 字典
    by:王健 at:2016-04-21
    """

    def toJSON(self, ex_parm=None, un_parm=None):
        """
        序列化成 dict类型
        by:王健 at:2015-1-29
        修改 刚刚修改过 的字符串 日期 bug
        by:王健 at:2015-2-3
        对数组类型的字段，优化转化
        by:王健 at:2015-06-27
        超出时间外的值，做默认值处理
        by:王健 at:2015-07-04
        修改语法 是否是None 应该用 is判断
        by:王健 at:2015-09-16
        增加timefield类型转换
        by: 魏璐 at:2016-02-24
        :return:
        """
        if ex_parm is None:
            ex_parm = []
        ex_parm.extend(self._meta.list_json)
        ex_parm.extend(self._meta.detail_json)
        ex_parm = set(ex_parm)
        if un_parm is not None:
            for p in un_parm:
                ex_parm.remove(p)
        ex_parm = list(ex_parm)
        ex_parm.sort()

        d = {}
        for attr in ex_parm:
            if getattr(self, attr, None) is None:
                d[attr] = None
            else:
                d[attr] = getattr(self, attr)
        return d


class ModefyMixin(object):
    """
    数据变动区别
    by:王健 at:2016-04-21
    """

    def copy_old(self):
        """
        复制对象
        by:王健 at:2016-04-21
        :return:
        """
        if self.pk:
            if getattr(self, '_old', None) is not None:
                raise Exception(u'The copy_old function only be used once')
            self._old = {}
            for field in self._meta.fields:
                self._old[field.attname] = getattr(self, field.attname, None)

    def compare_old(self):
        """
        比较新旧对象
        by:王健 at:2016-04-21
        :return:
        """
        if getattr(self, '_old', None) is None:
            if self.pk:
                raise Exception(u'The copy_old function is not yet in use')
            else:
                return True, {}
        diff_attr = {}
        for key, value in self._old.items():
            if value != getattr(self, key, None):
                diff_attr[key] = (value, getattr(self, key, None))
        return False, diff_attr

    def clean_old(self):
        """
        清除比较数据
        by:王健 at:2016-04-23
        :return:
        """
        if getattr(self, '_old', None) is not None:
            del self._old


class BaseModel(models.Model, JSONBaseMixin, ModefyMixin):
    """
    组织基础Model类
    by:王健 at:2016-04-18
    """
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=u'是否删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'是否删除')

    objects = ValuesQuerySet.as_manager()

    class Meta:
        abstract = True
        list_json = []
        detail_json = []

    def __unicode__(self):
        if hasattr(self, 'name'):
            return u'$s#%s' % (self.pk, self.name)
        else:
            raise Exception(u'需要重载 __unicode__ 函数')

    def save(self, **kwargs):
        super(BaseModel, self).save(**kwargs)
        self.clean_old()