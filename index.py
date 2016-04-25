# -*- coding:utf-8 -*-
import logging

import os
import sys
import traceback
import fcntl
import datetime
import django

sys.argv = [__file__]
os.environ['DJANGO_SETTINGS_MODULE'] = 'liyuoa_pm.settings'

path = os.path.dirname(os.path.abspath(__file__)) + '/liyuoa_pm'
if path not in sys.path:
    sys.path.insert(1, path)


def out_init_log(msg):
    BASE_DIR = os.path.dirname(__file__)

    # 创建日志目录
    # by: 范俊伟 at:2015-06-23
    dir = os.path.join(BASE_DIR, 'static_all')
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = os.path.join(dir, 'init.log')
    file = open(path, 'a')
    file.write("%s\n" % str(msg))
    file.close()


from django.core.wsgi import get_wsgi_application
from bae.core.wsgi import WSGIApplication

from django.core.management import execute_from_command_line
# 增加文件锁
# by: 范俊伟 at:2015-08-06
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'init.lock'), 'w') as fp:
    fcntl.flock(fp, fcntl.LOCK_EX)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out_init_log('run at:' + now)
    out_init_log('django version:' + str(django.VERSION))
    # 自动执行collectstatic
    # by: 范俊伟 at:2015-06-23
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        out_init_log('collectstatic complete')
    except Exception, e:
        out_init_log(traceback.format_exc())

    # 自动执行syncdb
    # by: 范俊伟 at:2015-07-15
    try:
        execute_from_command_line(['manage.py', 'syncdb', '--noinput'])
        out_init_log('syncdb complete')
    except Exception, e:
        out_init_log(traceback.format_exc())

    # 自动执行syncdb
    # by: 范俊伟 at:2015-07-15
    try:
        execute_from_command_line(['manage.py', 'sync_appinfo_and_role', '--noinput'])
        out_init_log('sync_appinfo_and_role complete')
    except Exception, e:
        out_init_log(traceback.format_exc())

    # 自动执行syncdb
    # by: 范俊伟 at:2015-07-15
    try:
        execute_from_command_line(['manage.py', 'sync_api_document', '--noinput'])
        out_init_log('sync_api_document complete')
    except Exception, e:
        out_init_log(traceback.format_exc())


application = WSGIApplication(get_wsgi_application(), stderr='log')
