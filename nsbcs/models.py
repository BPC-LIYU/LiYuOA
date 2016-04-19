# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
import os
import urllib
import uuid
from qiniu.services.storage import uploader
import requests
from Need_Server import settings
from Need_Server.settings import QN_AK, QN_SK, QN_BUCKET_CONFIG, QN_PRIVATE_BUCKET
import qiniu
from util.basemodel import JSONBaseMixin

__author__ = u'王健'
from django.db import models
from django.utils import timezone


qn_auth = qiniu.Auth(QN_AK, QN_SK)

NS_FILE_GROUP_TYPE_SYS = 0
NS_FILE_GROUP_TYPE_USER = 1
NS_FILE_GROUP_TYPE_COMPANY = 3

NS_FILE_GROUP_TYPE_CHOICES = [
    (NS_FILE_GROUP_TYPE_SYS, u'系统图片'),
    (NS_FILE_GROUP_TYPE_USER, u'用户图片'),
    (NS_FILE_GROUP_TYPE_COMPANY, u'组织图片'),
]


class NsFile(models.Model, JSONBaseMixin):
    """
    附件基础类
    by:王健 at:2015-1-28
    添加七牛存储的 bucket
    by:王健 at:2015-3-24
    增加img_size字段
    by: 范俊伟 at:2015-04-09
    编码中文文件名
    by: 范俊伟 at:2015-04-13
    增加文件所属云盘目录字段
    by:王健 at:2015-10-28
    is_copy 字段描述文件是否在数据删除是是否删除七牛文件
    by:王健 at:2015-10-31
    去除is_copy 字段，七牛上冗余存储
    by:王健 at:2015-10-31
    """

    name = models.CharField(max_length=50, verbose_name=u'附件名称')
    create_time = models.DateTimeField(default=timezone.now, verbose_name=u'创建时间')
    fileurl = models.CharField(max_length=255, verbose_name=u'文件存储位置')
    filetype = models.CharField(max_length=20, verbose_name=u'文件类型')
    size = models.BigIntegerField(default=0, verbose_name=u'文件大小')
    file_status = models.BooleanField(default=False, verbose_name=u'状态', help_text=u'True 以保存,False 未保存')
    bucket = models.CharField(default=QN_PRIVATE_BUCKET, max_length=20, verbose_name=u'是否开放')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, verbose_name=u'作者', help_text=u'上传人')
    img_size = models.CharField(max_length=20, null=True, verbose_name=u'图片大小', help_text=u'格式:80x80')
    project = models.ForeignKey('liyu_organization.Organization', null=True, verbose_name=u'隶属项目', help_text=u'隶属项目')
    cloud_disk = models.ForeignKey('needserver.CloudDisk', null=True, verbose_name=u'隶属云盘目录')
    group_type = models.IntegerField(default=NS_FILE_GROUP_TYPE_SYS, choices=NS_FILE_GROUP_TYPE_CHOICES)

    def get_url(self, fop=None, expires=3600):
        """
        T 取个整数，方便单元测试
        by:王健 at:2015-1-30
        修改 本机头像的 url
        by:王健 at:2015-3-6
        增加七牛云存储
        by: 范俊伟 at:2015-04-08
        七牛云存储增加处理数据功能
        by: 范俊伟 at:2015-04-08
        增肌超时时间设定
        by: 范俊伟 at:2015-08-28
        :return:
        """
        if self.fileurl.find('/static/headicon') == 0:
            return 'http://%s%s' % ('www.tjeasyshare.com', self.fileurl)
        else:
            config = QN_BUCKET_CONFIG.get(self.bucket)
            if not config:
                raise Exception(self.bucket + ':未知的bucket')

            domain = config.get('domain')
            is_private = config.get('is_private')
            url = domain + self.fileurl
            params = []
            if fop:
                params.append(fop)

            params.append("attname=" + urllib.quote(self.name.encode('utf-8')))
            url = url + '?' + '&'.join(params)
            if is_private:
                url = qn_auth.private_download_url(url, expires=expires)
            return url

    def get_thumbnail(self):
        """
        返回缩略图
        by: 范俊伟 at:2016-02-18
        :return:
        """
        filetype = self.filetype
        if filetype == 'bmp' or filetype == 'jpg' or filetype == 'jpeg' or filetype == 'png' or filetype == 'gif':
            return self.get_url('imageView2/5/w/180/h/140', expires=3600 * 24 * 365 * 10)
        elif filetype == 'mp4':
            return self.get_url('vframe/jpg/offset/3/rotate/auto', expires=3600 * 24 * 365 * 10)
        else:
            return self.get_url()

    def get_qn_post_url(self):
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
        # try:
        # bucket = bcs.bucket(self.bucket)
        # o1 = bucket.object(self.fileurl)
        # result = o1.delete()
        # except:
        # pass
        key = self.fileurl
        bucket = self.bucket
        r = super(NsFile, self).delete(*args, **kwargs)
        bucket_manage = qiniu.BucketManager(qn_auth)
        ret, info = bucket_manage.delete(bucket, key)
        return r

    def copy(self):
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
        newobj.file_status = self.file_status
        newobj.bucket = self.bucket
        newobj.user = self.user
        newobj.img_size = self.img_size
        newobj.project = self.project
        newobj.company = self.company
        newobj.group_type = self.group_type
        bucket_manage = qiniu.BucketManager(qn_auth)
        ret, info = bucket_manage.copy(self.bucket, self.fileurl, newobj.bucket, newobj.fileurl)

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

    def check_file(self):
        """
        检查文件是否在bcs上
        by:王健 at:2015-1-26
        修改dic读取错误
        by:范俊伟 at:2015-01-26
        :return:
        """
        # todo:改为使用七牛
        return True

    def save(self, *args, **kwargs):
        """
        重载save函数,获取图片分辨率
        by: 范俊伟 at:2015-04-09
        """
        from util.tools import common_except_log

        if self.file_status and self.img_size == None:
            try:
                url = self.get_url('imageInfo')
                response = requests.get(url)
                data = response.json()
                error = data.get('error')
                if error and error.find('unsupported format') != -1:
                    self.img_size = '0x0'
                else:
                    width = data.get('width')
                    height = data.get('height')
                    if width and height:
                        self.img_size = '%dx%d' % (width, height)
            except:
                common_except_log()

        if self.file_status and not self.size:
            try:
                bucket_manage = qiniu.BucketManager(qn_auth)
                ret, info = bucket_manage.stat(self.bucket, self.fileurl)
                if ret:
                    self.size = ret.get('fsize')
            except:
                common_except_log()

        return super(NsFile, self).save(*args, **kwargs)

    def toJSON(self):
        res = super(NsFile, self).toJSON()
        if not self.cloud_disk:
            res['cloud_disk'] = 0
        if self.name:
            n, ext = os.path.splitext(self.name)
            res['not_ext_name'] = n
            res['ext'] = ext
        res['url'] = self.get_url()
        return res

    @staticmethod
    def update_file_status(id, user=None, project=None, company=None):
        """
        更新文件状态
        by: 范俊伟 at:2015-08-28
        修改保存
        by: 范俊伟 at:2015-09-02
        :param id:
        :param user:
        :param project:
        :param company:
        :return:
        """
        for i in NsFile.objects.filter(pk=id):
            i.file_status = True
            if company:
                i.company = company
            if user:
                i.user = user
            if project:
                i.project = project
            i.save()
            return i


class FileDownloadRecord(models.Model, JSONBaseMixin):
    """
    文件下载记录
    by:王健 at:2015-10-31
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'下载用户')
    download_time = models.DateTimeField(default=timezone.now, verbose_name=u'下载时间')
    nsfile = models.ForeignKey('nsbcs.NsFile', verbose_name=u'下载的文件')
