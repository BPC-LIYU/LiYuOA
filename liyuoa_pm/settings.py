#coding=utf-8
"""
Django settings for liyuoa_pm project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys


# 解决 字符编码问题
# by:王健 at:2015-3-10
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs

codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&u%=za0yuyxr04gw(d7r9+pw6g=(hnw6$&yfly5r9ryk!#$v@$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

ENVIRONMENT = 'aliyun'
if 'SERVER_SOFTWARE' in os.environ:
    ENVIRONMENT = 'baidu'
elif 'mac_dev' in os.environ:
    ENVIRONMENT = 'develop'
elif 'win_dev' in os.environ:
    ENVIRONMENT = 'develop'
elif 'fjw_dev' in os.environ:
    ENVIRONMENT = 'fjw_dev'
# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'liyuoa',
    'liyu_organization',
    'clouddisk',
    'nsbcs',
    'liyuim',
)

MIDDLEWARE_CLASSES = (
    'util.middleware.ETagMiddleware',
    'util.middleware.CorsMiddleware',
    'util.middleware.GlobRequestMiddleware',
    'util.middleware.SessionTransferMiddleware',
    'util.middleware.UserAgentMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'util.middleware.CustomAuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'util.error_middle.ExceptionMiddleware',
)

ROOT_URLCONF = 'liyuoa_pm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'liyuoa_pm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'


AUTH_USER_MODEL = "liyuoa.LYUser"

USER_ICON_BG_COLORS = [
    '#4046ba',
    '#5b6bb8',
    '#5c59f1',
    '#00a0e9',
    '#74bef1',
    '#317a82',
    '#78919d',
    '#8c97cb',
    '#24b0cb',
    '#9fb0af',
    '#9274d4',
    '#b8a0dc',
    '#097c25',
    '#80cf76',
    '#3ccebb',
    '#8bddae',
    '#b1d337',
    '#a0887c',
    '#ca1888',
    '#e5004f',
    '#f65e8d',
    '#f35c5c',
    '#f98463',
    '#f9c01c',
]

# 七牛ak sk
# by:王健 at:2016-04-20
QN_AK = ''

QN_SK = ''

QN_BUCKET_CONFIG = {

}

QN_PUBLIC_BUCKET = ''
QN_PRIVATE_BUCKET = ''

HOST_URL = '0.0.0.0:8001'

NEED_MONGODB_HOST="mongodb://0.0.0.0:27017/liyuim?"


# **********************************************************
# **               注意将所有配置添加到此行之前               **
# **********************************************************
# 执行子配置
# by: 范俊伟 at:2015-06-01
etc_path = "/etc/ttjd/cfg.py"
if os.path.exists(etc_path):
    file = open(etc_path, 'r')
    text = file.read()
    file.close()
    try:
        exec (text)
    except Exception, e:
        print e
elif ENVIRONMENT:
    settings_path = os.path.join(BASE_DIR, 'liyuoa_pm', 'settings_%s.py' % ENVIRONMENT)
    if os.path.exists(settings_path):
        file = open(settings_path, 'r')
        text = file.read()
        file.close()
        try:
            exec (text)
        except Exception, e:
            print e
