# coding=utf-8
# Date: 15/1/29'
# Email: wangjian2254@icloud.com

import datetime
from django.db import models
import django.db.models.options as options

from util.model_tools import page_obj_query

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('list_json', 'detail_json')

__author__ = u'王健'


class ValuesQuerySet(models.QuerySet):
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

        ex_parms.extend(self.model.Meta.list_json)
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
        ex_parms.extend(self.model.Meta.detail_json)
        return self.list_json(ex_parms, un_parms)

    def get_serializer(self):
        """
        序列化 obj
        by:王健 at:2016-04-19
        :return:
        """
        try:
            return self.detail_json()[0]
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


class BaseModel(models.Model):
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
