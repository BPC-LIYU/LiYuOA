#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午8:44
# file:appinfo_sync_tools.py
# Email: wangjian2254@icloud.com
# Author: 王健
import os
import urllib
import uuid

import qiniu
from django.conf import settings
from qiniu.services.storage import uploader

from util.basemodel import BaseModel
from util.middleware import getHost

__author__ = u'王健'

from django.db import models

try:
    qn_auth = qiniu.Auth(settings.QN_AK, settings.QN_SK)
except:
    pass


class NsFile(BaseModel):
    """
    只保存文件基本信息
    by:王健 at:2016-04-29
    """

    name = models.CharField(max_length=50, verbose_name=u'附件名称')
    fileurl = models.CharField(max_length=255, verbose_name=u'文件存储位置')
    filetype = models.CharField(max_length=20, verbose_name=u'文件类型')
    size = models.BigIntegerField(default=0, verbose_name=u'文件大小')
    bucket = models.CharField(blank=True, max_length=20, verbose_name=u'位置')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=u'作者', help_text=u'上传人')
    # org = models.ForeignKey('liyu_organization.Organization', null=True, verbose_name=u'隶属项目', help_text=u'隶属项目')
    # person = models.ForeignKey('liyu_organization.Person', null=True, verbose_name=u'隶属组织成员', help_text=u'隶属项目')
    # cloud_disk = models.ForeignKey('clouddisk.CloudDisk', null=True, verbose_name=u'隶属云盘目录')
    access_type = models.CharField(default="public", max_length=10, db_index=True)
    file_status = models.BooleanField(default=False, db_index=True)

    class Meta:
        list_json = ['name', 'fileurl', 'bucket', 'id', 'filetype', 'size']
        detail_json = ['create_time', 'is_active', 'user_id']

    @staticmethod
    def get_url(fileurl, bucket, name, fop=None, expires=3600):
        """
        获取下载url
        by:王健 at:2016-04-20
        :param fileurl: 存储uri
        :param bucket: 所在空间
        :param name: 上传名字
        :param fop:
        :param expires:
        :return:
        """

        if fileurl.find('/static/headicon') == 0:
            return 'http://%s%s' % (getHost(), fileurl)
        else:
            config = settings.QN_BUCKET_CONFIG.get(bucket)
            if not config:
                raise Exception('%s:未知的bucket' % bucket)

            domain = config.get('domain')
            is_private = config.get('is_private')
            url = '%s%s' % (domain, fileurl)
            params = []
            if fop:
                params.append(fop)

            params.append("attname=" + urllib.quote(name.encode('utf-8')))
            url = url + '?' + '&'.join(params)
            if is_private:
                url = qn_auth.private_download_url(url, expires=expires)
            return url

    @staticmethod
    def get_thumbnail(fileurl, bucket, name, filetype):
        """
        返回缩略图
        by: 范俊伟 at:2016-02-18
        :return:
        """
        if filetype.lower() in ['bmp', 'jpg', 'jpeg', 'png', 'gif']:
            return NsFile.get_url(fileurl, bucket, name, 'imageView2/5/w/180/h/140', expires=3600 * 24 * 365 * 10)
        elif filetype == 'mp4':
            return NsFile.get_url(fileurl, bucket, name, 'vframe/jpg/offset/3/rotate/auto',
                                  expires=3600 * 24 * 365 * 10)
        else:
            return NsFile.get_url(fileurl, bucket, name)

    @staticmethod
    def get_qn_post_url():
        """
        获取七牛post url
        by: 范俊伟 at:2015-04-08
        :return:
        """
        return 'http://upload.qiniu.com/'

    def get_qn_params(self):
        """
        获取七牛post 参数
        by: 范俊伟 at:2015-04-08
        兼容IE上传
        by: 范俊伟 at:2015-07-30
        :return:
        """
        token = qn_auth.upload_token(self.bucket, expires=3600 * 24)
        params = {'token': token, 'key': self.fileurl, "accept": "text/plain; charset=utf-8"}
        return params

    def delete(self, *args, **kwargs):
        """
        七牛删除
        by: 范俊伟 at:2015-07-30
        :param args:
        :param kwargs:
        :return:
        """

        key = self.fileurl
        bucket = self.bucket
        r = super(NsFile, self).delete(*args, **kwargs)
        bucket_manage = qiniu.BucketManager(qn_auth)
        ret, info = bucket_manage.delete(bucket, key)
        return r

    def copy(self, user, bucket):
        """
        七牛复制
        by: 闫宇 at:2015-11-01
        :param args:
        :param kwargs:
        :return:
        """
        newobj = NsFile()
        newobj.name = self.name
        path, fname = os.path.split(self.fileurl)
        name, ext = os.path.splitext(fname)
        newobj.fileurl = "%s/%s" % (path, str(uuid.uuid1()) + ext)
        newobj.filetype = self.filetype
        newobj.size = self.size
        newobj.bucket = bucket
        newobj.user = user
        # newobj.person = person
        # newobj.org = org
        bucket_manage = qiniu.BucketManager(qn_auth)
        ret, info = bucket_manage.copy(self.bucket, self.fileurl, newobj.bucket, newobj.fileurl)
        if ret:
            newobj.is_active = True
            newobj.save()
        return newobj

    def putdata(self, data):
        """
        把文件推送到bcs
        by:王健 at:2015-1-28
        把文件推送到七牛
        by: 范俊伟 at:2015-04-14
        :param data:
        :return:
        """
        key = self.fileurl
        token = qn_auth.upload_token(self.bucket, expires=3600 * 24)
        ret, info = uploader.put_data(token, key, data, check_crc=True)
        return ret['key'] == key

    def save(self, *args, **kwargs):
        """
        重载save函数,获取图片分辨率
        by: 范俊伟 at:2015-04-09
        """
        from util.tools import common_except_log
        if self.file_status and not self.size:
            try:
                bucket_manage = qiniu.BucketManager(qn_auth)
                ret, info = bucket_manage.stat(self.bucket, self.fileurl)
                if ret:
                    self.size = ret.get('fsize')
            except:
                common_except_log()

        return super(NsFile, self).save(*args, **kwargs)

    def update_file_status(self):
        """
        更新文件状态
        by:王健 at:2016-04-20
        :param self:
        :return:
        """

        self.file_status = True

        self.save()

