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

from liyuoa.models import AppApi, AppApiCareUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            l = urlAll('^', settings.ROOT_URLCONF)
            urls = []
            for url, fun in l:
                print url, ":", fun
                a = fun.split('.')
                fun_name = a[-1]
                fun_path = os.path.join(settings.BASE_DIR, *a[:-1])
                check, response_check, doclist, code = get_fun_info(fun_path, fun_name)
                api = save_fun_api(url, funname=fun_name, funpath=fun_path, code=code, doclist=doclist)
                save_fun_doc(api, doclist=doclist)
                save_fun_check(api, check=check)
                save_fun_check_response(api, response_check=response_check)

                urls.append(url)
            formate_js_api()
            AppApi.objects.exclude(url__in=urls).update(is_active=False, update_time=timezone.now())
            AppApiCareUser.objects.exclude(api__url__in=urls).update(is_active=False, update_time=timezone.now())


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

    # 找出结果校验的位置
    check_response_start = 0
    check_response_end = 0
    for i, (index, code_first_char, code) in enumerate(key_list):
        if code_first_char == '@' and code.find('@check_response_results') >= 0:
            check_response_start = index
            check_response_end = key_list[i + 1][0]
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
    fun_response_check = ''.join(code_list[check_response_start: check_response_end])

    return fun_check, fun_response_check, fun_doc, fun_code


def save_fun_api(url, funname, funpath, code, doclist):
    """
    修改保存api信息
    :param doclist:
    :param url:
    :param funname:
    :param funpath:
    :param code:
    :return:
    """
    from liyuoa.models import AppApi, AppApiCareUser, AppInfo

    # 新建或修改api
    if AppApi.objects.filter(url=url).exists():
        api = AppApi.objects.get(url=url)
        api.copy_old()
    else:
        api = AppApi()
    m = url.split('/')[0]
    try:
        api.app = AppInfo.objects.get(flag=m, is_active=True)
    except AppInfo.DoesNotExist:
        api.app = None
        print m, ':', '没有appinfo'

    namespace = '%s.%s' % (funpath, funname)
    if api.app:
        namespace = namespace[namespace.find(api.app.namespace):]
    api.url = url
    api.is_active = True
    api.namespace = namespace
    api.code_content = code
    api.name = doclist[0]
    if url.rfind('_list') == len(url) - 5:
        api.response_type = 'list'
    else:
        api.response_type = 'dict'
    created, diff = api.compare_old()
    if created or diff:
        api.save()
        AppApiCareUser.objects.filter(api=api).update(is_confirm=False, update_time=timezone.now())
    return api


def save_fun_doc(api, doclist):
    """
    保存接口修改的注释
    :param api:
    :param doclist:
    :return:
    """
    from liyuoa.models import AppApiComment
    # 代码修改记录 保存入评论表
    try:
        last_comment = AppApiComment.objects.filter(api=api, source=0).order_by('-id')[0]
    except:
        last_comment = None
    dl = []
    d_start = 0
    for i, line in enumerate(doclist):
        if line.strip().find(':return:') == 0:
            d_start = i+1
        if line.strip().find('by:') == 0:
            dl.append((i, [x.strip() for x in line.replace('by:', '').split('at:') if x]))
    comment_dict_list = []

    # 找到最后保存的一个代码修改评论
    comment_index = 0
    for i, (line_index, auth_arr) in enumerate(dl):
        line = ''.join(doclist[d_start:line_index])
        auth = auth_arr[0]
        date = datetime.datetime.strptime(auth_arr[1], '%Y-%m-%d')
        comment_dict_list.append({"content": line, "auth": auth, "date": date})
        d_start = line_index + 1
        if last_comment and last_comment.content == line:
            comment_index = i+1

    # 从最后一个修改评论开始新建
    for i in range(comment_index, len(comment_dict_list)):
        a = AppApiComment()
        a.api = api
        a.content = comment_dict_list[i]['content']
        a.username = comment_dict_list[i]['auth']
        a.source = 0
        a.create_time = comment_dict_list[i]['date']
        a.save()


def save_fun_check(api, check):
    """
    将当前的参数校验文档保存
    by:王健 at:2016-04-20
    :param api:
    :param check:
    :return:
    """
    from liyuoa.models import AppApiParameter

    if not check:
        AppApiParameter.objects.filter(api=api).update(is_active=False)
        return
    # 参数解析成字典
    parameter = None
    try:
        parameter = eval(check.replace('@check_request_parmes', 'formate_parameter'))
    except:
        print api.namespace, ":", check, ': error'

    if parameter is None:
        return

    # 新建或修改参数
    parameterlist = []
    for p in AppApiParameter.objects.filter(api=api):
        p.copy_old()
        p.is_active = False
        parameterlist.append(p)

    for name, value in parameter.items():
        old_parameter = False
        for p in parameterlist:
            if name == p.name:
                old_parameter = True
                title = value[0]
                check_args = value[1].split(',')
                if len(value) == 3:
                    p.default = value[2]
                else:
                    p.default = None
                p.title = title
                p.is_required = 'r' in check_args
                if 'r' not in check_args:
                    parm_type = ','.join(check_args)
                else:
                    check_args.remove('r')
                    parm_type = ','.join(check_args)
                p.parm_type = parm_type
                p.is_active = True
                created, diff = p.compare_old()
                if created or diff:
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
            if len(value) == 3:
                p.default = value[2]
            else:
                p.default = None
            if 'r' not in check_args:
                parm_type = ','.join(check_args)
                p.is_required = False
            else:
                p.is_required = True
                check_args.remove('r')
                parm_type = ','.join(check_args)
            p.parm_type = parm_type
            p.save()
    for p in parameterlist:
        created, diff = p.compare_old()
        if created or diff:
            p.save()


def save_fun_check_response(api, response_check):
    """
    将当前的返回值校验保存
    by:王健 at:2016-04-20
    :param api:
    :param response_check:
    :return:
    """
    from liyuoa.models import AppApiResponse

    if not response_check:
        AppApiResponse.objects.filter(api=api).update(is_active=False)
        return
    # 参数解析成字典
    parameter = eval(response_check.replace('@check_response_results', 'formate_parameter'))

    if parameter is None:
        return

    # 新建或修改参数
    parameterlist = []
    for p in AppApiResponse.objects.filter(api=api):
        p.copy_old()
        p.is_active = False
        parameterlist.append(p)

    for name, value in parameter.items():
        old_parameter = False
        for p in parameterlist:
            if name == p.name:
                old_parameter = True
                title = value[0]
                check_args = value[1].split(',')
                p.title = title
                if check_args:
                    p.response_type = ','.join(check_args)
                else:
                    p.response_type = '字符串'
                p.is_active = True
                created, diff = p.compare_old()
                if created or diff:
                    p.save()
                parameterlist.remove(p)
                break

        if not old_parameter:
            title = value[0]
            check_args = value[1].split(',')
            p = AppApiResponse()
            p.api = api
            p.name = name
            p.title = title
            if check_args:
                p.response_type = ','.join(check_args)
            else:
                p.response_type = '字符串'
            p.save()
    for p in parameterlist:
        created, diff = p.compare_old()
        if created or diff:
            p.save()


def formate_js_api():
    """
    生成js api 接口调用代码
    by:王健 at:2016-04-25
    :param api:
    :return:
    """

    jsappfun = """
            '%s': {
                %s
            },
    """
    jsapifun = """
                // %s
                '%s': 'func',
            """
    from liyuoa.models import AppApiParameter, AppInfo
    applist = []
    for app in AppInfo.objects.filter(is_active=True).order_by('flag'):
        apilist = []
        for api in AppApi.objects.filter(app=app, is_active=True).order_by('url'):

            func = api.url.split("/")[1]
            parmlist = [' %s:%s' % (p.name, p.title) for p in AppApiParameter.objects.filter(api=api, is_active=True).order_by('name')]
            apilist.append(jsapifun % (','.join(parmlist), func))
        applist.append(jsappfun % (app.flag, ''.join(apilist)))
    apijs = file('api.js', 'w')
    apijs.write(jsfile_template % ''.join(applist))
    apijs.close()




def formate_parameter(**kwargs):
    return kwargs


jsfile_template = """service_app
    .factory("api", function (httpReq) {
        var apis = {
            %s
        };

        function init_api(parents, dic) {
            var url, p;
            _(dic).each(function (value, key) {
                p = parents.slice(0);//数组拷贝
                p.push(key);
                if (value === 'func') {
                    url = "/" + p.join('/');
                    dic[key] = httpReq.bind(null, url);
                }
                else {
                    init_api(p, value);
                }

            })
        }

        init_api([], apis);

        return apis;
    });

"""