#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/20 下午2:20
# file:urls.py
# Email: wangjian2254@icloud.com
# Author: 王健


from django.conf.urls import patterns, url

urlpatterns = patterns('liyuoa',
                       url('^logout$', 'views.logout'),
                       url('^login$', 'views.login'),
                       url('^check_login$', 'views.check_login'),
                       url('^reg_user$', 'views.reg_user'),
                       url('^simple_login$', 'views.simple_login'),
                       url('^sync_cookie$', 'views.sync_cookie'),
                       url('^change_password_by_code$', 'views.change_password_by_code'),
                       url('^change_password$', 'views.change_password'),
                       url('^send_sms_code$', 'views.send_sms_code'),
                       url('^send_sms_code_reg$', 'views.send_sms_code_reg'),

                       # 二维码
                       url('^qrcode_login_check$', 'views_qrcode.qrcode_login_check'),
                       url('^qrcode_login_scan$', 'views_qrcode.qrcode_login_scan'),
                       url('^qrcode_login_string$', 'views_qrcode.qrcode_login_string'),
                       url('^my_userinfo$', 'views.my_userinfo'),
                       )
