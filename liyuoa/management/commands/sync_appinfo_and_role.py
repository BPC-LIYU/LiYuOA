#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午8:44
# file:appinfo_sync_tools.py
# Email: wangjian2254@icloud.com
# Author: 王健
from django.conf import settings
from django.core.management import BaseCommand
import importlib

from django.db import transaction


class Command(BaseCommand):

    def handle(self, *args, **options):
        with transaction.atomic():
            for app in settings.INSTALLED_APPS:
                try:
                    if app.find('django') == 0:
                        continue
                    m = importlib.import_module("%s.app_config" % app)
                    sync_app_info_and_role(m.used_app, app)
                    print app, u': sync success'
                except ImportError as e:
                    # common_except_log()
                    print app, u': sync fail'
                    pass


def sync_app_info_and_role(used_app, APP_NAMESPACE):
    """
    同步应用和角色信息
    by:王健 at:2016-04-19
    :param used_app:
    :param APP_NAMESPACE:
    :return:
    """
    from liyuoa.models import AppInfo
    from liyuoa.models import AppRole
    applist = []
    for app in AppInfo.objects.filter(namespace=APP_NAMESPACE):
        app.copy_old()
        applist.append(app)

    rolelist = []
    for role in AppRole.objects.filter(app__namespace=APP_NAMESPACE):
        role.copy_old()
        rolelist.append(role)
    for app_cls in used_app:
        has_app = False
        for app in applist:
            if app.flag == app_cls.flag:
                has_app = True
                app.name = app_cls.name
                app.is_active = True
                app.type_flag = app_cls.type_flag
                app.is_show = app_cls.is_show
                app.desc = app_cls.desc

                for role_cls in app_cls.role_list:
                    has_role = False
                    for role in rolelist:
                        if role.role == role_cls.role and role.app_id == app.id:
                            has_role = True
                            role.name = role_cls.role_name
                            role.desc = role_cls.role_desc
                            role.is_active = True

                    # 应用下创建新的角色
                    if not has_role:
                        role = AppRole()
                        role.role = role_cls.role
                        role.name = role_cls.role_name
                        role.desc = role_cls.role_desc
                        role.app = app
                        role.save()

        # 创建新的应用和角色
        if not has_app:
            app = AppInfo()
            app.flag = app_cls.flag
            app.name = app_cls.name
            app.type_flag = app_cls.type_flag
            app.is_show = app_cls.is_show
            app.desc = app_cls.desc
            app.namespace = APP_NAMESPACE
            app.save()
            for role_cls in app_cls.role_list:
                role = AppRole()
                role.role = role_cls.role
                role.name = role_cls.role_name
                role.desc = role_cls.role_desc
                role.app = app
                role.save()

    for app in applist:
        created, diff = app.compare_old()
        if created or diff:
            app.save()
            print app.name, ":", "发生变化"
    for role in rolelist:
        created, diff = role.compare_old()
        if created or diff:
            role.save()
            print role.name, ":", "发生变化"
