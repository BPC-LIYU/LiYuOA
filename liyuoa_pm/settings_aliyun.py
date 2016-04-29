# coding=utf-8
# Date: 15/5/21
# Time: 11:21
# Email:fanjunwei003@163.com

HOST_URL = '121.42.211.17'

NEED_MONGODB_HOST = "mongodb://3885ef8a96a73e17dbfa0e766de2ce08:B5cb0046c2f2d9578597861c7c6e6b6c@mongo.duapp.com:8908/DaPCQtSLxVnyKsocjgkm?"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'liyuoa',  # Or path to database file if using sqlite3.
        'USER': 'liyuoa',  # Not used with sqlite3.
        'PASSWORD': 'liyuoa',  # Not used with sqlite3.
        'HOST': 'rdsmf2ybzzezumn.mysql.rds.aliyuncs.com',
        # 'HOST': 'sub1437356138367-rdsmizy48ivz81cwa9uvt.mysql.rds.aliyuncs.com',
        # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        'ATOMIC_REQUEST': True,
        # 'OPTIONS': {'charset': 'utf8mb4'},
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'LOCATION': '3fed0c36dc1e4d77.m.cnqdalicm9pub001.ocs.aliyuncs.com:11211',
        'OPTIONS': {
            'username': '3fed0c36dc1e4d77',
            'password': 'LiYuOA01',
            'MAX_ENTRIES': 10000 * 300
        }
    }
}
# session 交由 memcache管理
# by:王健 at:2015-07-14
# 修改session的保存期限
# by:王健 at:2015-07-15
SESSION_ALIYUN_HOST = '3fed0c36dc1e4d77.m.cnqdalicm9pub001.ocs.aliyuncs.com:11211'
SESSION_ALIYUN_OPTIONS = {'OPTIONS': {
    'username': '3fed0c36dc1e4d77',
    'password': 'LiYuOA01',
    'MAX_ENTRIES': 10000 * 300
},
    'timeout': 3600 * 24 * 30}
# session 交由 redis 管理
# by:尚宗凯 at:2015-3-8
SESSION_ENGINE = 'aliyun_session.session'
SESSION_OCS_PREFIX = 'aliyun_session_liyuoa'


MQTT_HOST = "0.0.0.0"
MQTT_PORT = 50051
