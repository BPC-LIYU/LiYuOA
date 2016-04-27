#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午8:44
# file:urls.py
# Email: wangjian2254@icloud.com
# Author: 王健

__author__ = u'王健'

from django.conf.urls import patterns, url

urlpatterns = patterns('liyu_organization',
                       url('^query_my_org_list$', 'views_org.query_my_org_list'),
                       url('^get_organization$', 'views_org.get_organization'),
                       url('^apply_organization$', 'views_org.apply_organization'),
                       url('^agree_organization$', 'views_org.agree_organization'),
                       url('^reject_organization$', 'views_org.reject_organization'),
                       url('^add_person_org$', 'views_org.add_person_org'),
                       url('^remove_person_org$', 'views_org.remove_person_org'),
                       url('^add_manager_org$', 'views_org.add_manager_org'),
                       url('^remove_manager_org$', 'views_org.remove_manager_org'),
                       url('^transfer_manager_org$', 'views_org.transfer_manager_org'),
                       url('^update_organization$', 'views_org.update_organization'),
                       url('^create_organization$', 'views_org.create_organization'),

                       url('^query_group_by_org_list$', 'views_group.query_group_by_org_list'),
                       url('^query_group_by_group_list$', 'views_group.query_group_by_group_list'),
                       url('^query_group_by_my_list$', 'views_group.query_group_by_my_list'),
                       url('^create_group$', 'views_group.create_group'),
                       url('^update_group$', 'views_group.update_group'),
                       url('^remove_charge_group$', 'views_group.remove_charge_group'),
                       url('^remove_aide_group$', 'views_group.remove_aide_group'),
                       url('^add_charge_group$', 'views_group.add_charge_group'),
                       url('^add_aide_group$', 'views_group.add_aide_group'),
                       url('^remove_group$', 'views_group.remove_group'),
                       url('^add_person_group$', 'views_group.add_person_group'),
                       url('^remove_person_group$', 'views_group.remove_person_group'),
                       url('^update_person_group$', 'views_group.update_person_group'),
                       url('^query_member_by_group_list$', 'views_group.query_member_by_group_list'),

                       url('^query_appinfo_by_org_list$', 'views_appinfo.query_appinfo_by_org_list'),
                       url('^query_not_used_appinfo_by_org_list$', 'views_appinfo.query_not_used_appinfo_by_org_list'),
                       url('^add_appinfo$', 'views_appinfo.add_appinfo'),
                       url('^remove_appinfo$', 'views_appinfo.remove_appinfo'),
                       url('^make_appinfo_permission$', 'views_appinfo.make_appinfo_permission'),
                       url('^query_user_permissions_list$', 'views_appinfo.query_user_permissions_list'),
                       url('^query_role_by_apps_list$', 'views_appinfo.query_role_by_apps_list'),


                       )
