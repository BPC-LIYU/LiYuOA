#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/21 下午2:21
# file: urls.py
# Email: wangjian2254@icloud.com
# Author: 王健


from django.conf.urls import patterns, url

urlpatterns = patterns('liyuoa.develop',
                       url('^query_all_app$', 'views_develop.query_all_app'),
                       url('^query_api_list$', 'views_develop.query_api_list'),
                       url('^query_appinfo_list$', 'views_develop.query_appinfo_list'),
                       url('^get_appinfo$', 'views_develop.get_appinfo'),
                       url('^query_appcareuser_list$', 'views_develop.query_appcareuser_list'),
                       url('^get_api$', 'views_develop.get_api'),
                       )
