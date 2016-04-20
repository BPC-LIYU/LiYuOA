#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/20 下午2:20
# file:urls.py
# Email: wangjian2254@icloud.com
# Author: 王健

__author__ = u'王健'

from django.conf.urls import patterns, url


urlpatterns = patterns('nsbcs',
                        # url添加$结束符
                        # by:王健 at:2015-1-21
                       url(r'^get_upload_files_url$', 'views_bcsfile.get_upload_files_url'),
                        # 检查文件是否在bcs中
                        # by:王健 at:2015-1-26
                       url(r'^get_file_url_public$', 'views_bcsfile.get_file_url_public'),
                       url(r'^get_file_url_private$', 'views_bcsfile.get_file_url_private'),
                       url(r'^upload_complete$', 'views_bcsfile.upload_complete'),

)