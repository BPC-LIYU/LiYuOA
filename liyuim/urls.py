#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午8:44
# file:urls.py
# Email: wangjian2254@icloud.com
# Author: 王健

__author__ = u'王健'

from django.conf.urls import patterns, url

urlpatterns = patterns('liyuim',
                       url('^query_my_friend_list$', 'views_friend.query_my_friend_list'),
                       url('^query_friendapply_list$', 'views_friend.query_friendapply_list'),
                       url('^apply_friend$', 'views_friend.apply_friend'),
                       url('^pass_friendapply$', 'views_friend.pass_friendapply'),
                       url('^add_friend$', 'views_friend.add_friend'),
                       url('^reject_friendapply$', 'views_friend.reject_friendapply'),
                       url('^modefy_friend_nickname$', 'views_friend.modefy_friend_nickname'),
                       url('^mark_friend_black$', 'views_friend.mark_friend_black'),
                       url('^mark_friend_muted$', 'views_friend.mark_friend_muted'),
                       url('^query_black_friend_list$', 'views_friend.query_black_friend_list'),


                       url('^query_my_talkgroup_list$', 'views_talkgroup.query_my_talkgroup_list'),
                       url('^query_group_by_flag_list$', 'views_talkgroup.query_group_by_flag_list'),
                       url('^create_talkgroup$', 'views_talkgroup.create_talkgroup'),
                       url('^get_talkgroup$', 'views_talkgroup.get_talkgroup'),
                       url('^query_talkgroup_member_list$', 'views_talkgroup.query_talkgroup_member_list'),
                       url('^quite_talkgroup$', 'views_talkgroup.quite_talkgroup'),
                       url('^dismiss_talkgroup$', 'views_talkgroup.dismiss_talkgroup'),
                       url('^remove_talkgroup$', 'views_talkgroup.remove_talkgroup'),
                       url('^add_talkgroup$', 'views_talkgroup.add_talkgroup'),
                       url('^apply_talkgroup$', 'views_talkgroup.apply_talkgroup'),
                       url('^pass_talkapply$', 'views_talkgroup.pass_talkapply'),
                       url('^reject_talkapply$', 'views_talkgroup.reject_talkapply'),
                       url('^add_talkgroup_manager$', 'views_talkgroup.add_talkgroup_manager'),
                       url('^remove_talkgroup_manager$', 'views_talkgroup.remove_talkgroup_manager'),
                       url('^transfer_talkgroup_manager$', 'views_talkgroup.transfer_talkgroup_manager'),
                       url('^update_nick_in_talkgroup$', 'views_talkgroup.update_nick_in_talkgroup'),
                       url('^update_info_in_talkgroup$', 'views_talkgroup.update_info_in_talkgroup'),

                       )
