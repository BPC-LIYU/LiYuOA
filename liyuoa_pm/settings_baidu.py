#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/28 上午8:44
# file: settings_baidu.py.py
# Email: wangjian2254@icloud.com
# Author: 王健
# coding=utf-8
# Date: 15/5/21
# Time: 11:21
# Email:fanjunwei003@163.com

HOST_URL = 'liyuoa.duapp.com'

NEED_MONGODB_HOST = "mongodb://3885ef8a96a73e17dbfa0e766de2ce08:B5cb0046c2f2d9578597861c7c6e6b6c@mongo.duapp.com:8908/DaPCQtSLxVnyKsocjgkm?"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'svridx531ja18ee',  # Or path to database file if using sqlite3.
        'USER': '3885ef8a96a73e17dbfa0e766de2ce08',  # Not used with sqlite3.
        'PASSWORD': 'B5cb0046c2f2d9578597861c7c6e6b6c',  # Not used with sqlite3.
        'HOST': 'svridx531ja18ee.mysql.duapp.com',
        # 'HOST': 'sub1437356138367-rdsmizy48ivz81cwa9uvt.mysql.rds.aliyuncs.com',
        # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '10444',  # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUEST': True,
        # 'OPTIONS': {'charset': 'utf8mb4'},
    }
}

SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS_HOST = 'redis.duapp.com'
SESSION_REDIS_PORT = 80
SESSION_REDIS_DB = 0
SESSION_REDIS_PASSWORD = "3885ef8a96a73e17dbfa0e766de2ce08-B5cb0046c2f2d9578597861c7c6e6b6c-urjKdPSgzQrZKYyNSEDk"
SESSION_REDIS_PREFIX = 'liyuoa_session'

CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis.duapp.com:80',
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': '3885ef8a96a73e17dbfa0e766de2ce08-B5cb0046c2f2d9578597861c7c6e6b6c-urjKdPSgzQrZKYyNSEDk',
            'MAX_ENTRIES': 20000
        },
    },
}
