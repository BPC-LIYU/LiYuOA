# coding=utf-8
# Date:2015/1/10
# Email:wangjian2254@gmail.com
__author__ = u'王健'

from django.conf.urls import patterns, url


urlpatterns = patterns('nsbcs',
                        #url添加$结束符
                        #by:王健 at:2015-1-21
                       url(r'^get_upload_files_url$', 'views_bcsfile.get_upload_files_url'),
                        #检查文件是否在bcs中
                        #by:王健 at:2015-1-26
                       url(r'^check_file_upload_status$', 'views_bcsfile.check_file_upload_status'),
                       url(r'^get_file_url$', 'views_bcsfile.get_file_url'),
                       url(r'^upload_complete$', 'views_bcsfile.upload_complete'),

)