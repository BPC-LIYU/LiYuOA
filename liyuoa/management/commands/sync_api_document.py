#!/usr/bin/env python
# encoding: utf-8
# Date: 16/4/19 下午8:44
# file:sync_api_document.py
# Email: wangjian2254@icloud.com
# Author: 王健
import datetime
import os

from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            l = urlAll('^', 'liyuoa_pm.urls')
            for url, fun in l:
                print url, ":", fun
                a = fun.split('.')
                fun_name = a[-1]
                fun_path = os.path.join(settings.BASE_DIR, *a[:-1])
                try:
                    check, doclist, code = get_fun_info(fun_path, fun_name)
                    save_fun_info(url, fun_name, fun_path, check, doclist, code)
                except Exception as e:
                    print "error:", url, fun
                    raise e


def urlAll(pattern, urlconf_name):
    if isinstance(urlconf_name, (str, unicode)):
        exec ('import %s' % urlconf_name)
        urlmod = eval(urlconf_name)
    else:
        urlmod = urlconf_name

    urlpatterns = urlmod.urlpatterns
    url_all = []
    for urlpattern in urlpatterns:
        newpattern = pattern + urlpattern.regex.pattern[1:]
        if newpattern[0] == '^':
            newpattern = newpattern[1:]
        if newpattern[-1] == '$':
            newpattern = newpattern[:-1]
        if hasattr(urlpattern, 'urlconf_name'):
            # 存在urls子模块，递归该方法
            url_all.extend(urlAll(newpattern, urlpattern.urlconf_name))
        else:
            url_all.append((newpattern, urlpattern._callback_str))

    return url_all


def get_fun_info(file_path, fun_name):
    """
    获取函数代码 获取函数__doc__
    by:王健 at:2016-04-20
    :param file_path:
    :return:
    """
    code_list = file('%s.py' % file_path).readlines()
    key_list = []
    # 找出关键点, 首行不缩进的 以 特定字符开头的 都是关键点
    for i, code in enumerate(code_list):

        code_first_char = code[0]
        if code_first_char in ['@', 'd', 'c', 'f', 'i']:
            key_list.append((i, code_first_char, code))
    # 找出函数体开始和结束的点, 重复函数要排除
    fun_end = 0
    fun_start = 0
    for i, (index, code_first_char, code) in enumerate(key_list):
        if code_first_char == 'd' and code.find('def %s(' % fun_name) >= 0:
            if len(key_list) == i + 1:
                fun_end = len(code_list)
            else:
                fun_end = key_list[i + 1][0]
                key_list = key_list[:i + 1]
            break
    key_list.reverse()
    for i, (index, code_first_char, code) in enumerate(key_list):
        if i > 0 and code_first_char in ['d', 'c', 'f', 'i']:
            fun_start = key_list[i - 1][0]
            key_list = key_list[:i]
            break
    key_list.reverse()

    # 找出参数校验的位置
    check_start = 0
    check_end = 0
    for i, (index, code_first_char, code) in enumerate(key_list):
        if code_first_char == '@' and code.find('@check_request_parmes') >= 0:
            check_start = index
            check_end = key_list[i + 1][0]
            break

    # 找出doc信息的位置
    fun_doc_start = 0
    fun_doc_end = 0
    for i in range(fun_start, fun_end):
        code = code_list[i]
        if code.find('"""') > 0 or code.find("'''") > 0:
            if fun_doc_start == 0:
                fun_doc_start = i + 1
            else:
                fun_doc_end = i
                break

    fun_code = ''.join(code_list[fun_start: fun_end])
    fun_doc = code_list[fun_doc_start: fun_doc_end]
    # check_code = []
    # for code in code_list[check_start: check_end]:
    #     check_code.append(code.strip())
    fun_check = ''.join(code_list[check_start: check_end])

    return fun_check, fun_doc, fun_code


def save_fun_info(url, funname, funpath, check, doclist, code):
    """
    将当前的文档保存
    by:王健 at:2016-04-20
    :param url:
    :param funname:
    :param funpath:
    :param check:
    :param doc:
    :param code:
    :return:
    """
    from liyuoa.models import AppApi, AppApiCareUser, AppInfo, AppApiParameter, AppApiReplay

    # 新建或修改api
    if AppApi.objects.filter(url=url).exists():
        api = AppApi.objects.get(url=url)
    else:
        api = AppApi()
    m = url.split('/')[0]
    try:
        api.app = AppInfo.objects.get(flag=m, is_active=True)
    except AppInfo.DoesNotExist:
        api.app = None
        print m, ':', '没有appinfo'

    namespace = '%s.%s' % (funpath, funname)
    change = False
    if api.url != url:
        api.url = url
        change = True
    if api.namespace != namespace:
        api.namespace = namespace
        change = True
    if api.code_content != code:
        api.code_content = code
        change = True
    if api.name != doclist[0]:
        api.name = doclist[0]
        change = True

    if change:
        api.save()
        AppApiCareUser.objects.filter(api=api).update(is_confirm=False, update_time=timezone.now())

    if not check:
        AppApiParameter.objects.filter(api=api).update(is_active=False)
        return
    # 参数解析成字典
    parameter = None
    try:
        parameter = eval(check.replace('@check_request_parmes', 'formate_parameter'))
    except:
        print namespace, ":", check, ': error'

    if parameter is None:
        return

    # 新建或修改参数
    parameterlist = []
    for p in AppApiParameter.objects.filter(api=api):
        p.is_active_old = p.is_active
        p.is_active = False

        parameterlist.append(p)

    for name, value in parameter.items():
        old_parameter = False
        for p in parameterlist:
            if name == p.name:

                old_parameter = True
                title = value[0]
                check_args = value[1].split(',')
                change = False
                if p.title != title:
                    p.title = title
                    change = True
                if p.is_required:
                    if 'r' not in check_args:
                        p.is_required = False
                        change = True
                else:
                    if 'r' in check_args:
                        p.is_required = True
                        change = True
                if 'r' not in check_args:
                    parm_type = ','.join(check_args)
                else:
                    check_args.remove('r')
                    parm_type = ','.join(check_args)
                if p.parm_type != parm_type:
                    p.parm_type = parm_type
                    change = True
                if not p.is_active_old:
                    p.is_active = True
                    change = True
                if change:
                    p.save()
                parameterlist.remove(p)
                break

        if not old_parameter:
            title = value[0]
            check_args = value[1].split(',')
            p = AppApiParameter()
            p.api = api
            p.name = name
            p.title = title
            if 'r' not in check_args:
                parm_type = ','.join(check_args)
                p.is_required = False
            else:
                p.is_required = True
                check_args.remove('r')
                parm_type = ','.join(check_args)
            p.parm_type = parm_type
            p.save()

    # 代码修改记录 保存入评论表
    try:
        last_replay = AppApiReplay.objects.filter(api=api, source=0).order_by('-id')[0]
    except:
        last_replay = None
    dl = []
    d_start = 0
    for i, line in enumerate(doclist):
        if line.strip().find(':return:') == 0:
            d_start = i
        if line.strip().find('by:') == 0:
            dl.append((i, [x.strip() for x in line.replace('by:', '').split('at:') if x]))
    replay_dict_list = []

    # 找到最后保存的一个代码修改评论
    replay_index = 0
    for i, (line_index, auth_arr) in enumerate(dl):
        line = ''.join(doclist[d_start:line_index])
        auth = auth_arr[0]
        date = datetime.datetime.strptime(auth_arr[1], '%Y-%m-%d')
        replay_dict_list.append({"content": line, "auth": auth, "date": date})
        d_start = line_index + 1
        if last_replay and last_replay.content == line:
            replay_index = i

    # 从最后一个修改评论开始新建
    for i in range(replay_index, len(replay_dict_list)):
        a = AppApiReplay()
        a.api = api
        a.content = replay_dict_list[i]['content']
        a.username = replay_dict_list[i]['auth']
        a.source = 0
        a.create_time = replay_dict_list[i]['date']
        a.save()


def formate_parameter(**kwargs):
    return kwargs
