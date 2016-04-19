# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
from django.conf import settings
from django.db import transaction
from django.http import Http404

from Need_Server.settings import QN_PUBLIC_BUCKET, QN_PRIVATE_BUCKET
from needserver.models import NSUser

__author__ = u'王健'

import uuid
from django.shortcuts import get_object_or_404

from nsbcs.models import NsFile, NS_FILE_GROUP_TYPE_SYS, NS_FILE_GROUP_TYPE_USER, NS_FILE_GROUP_TYPE_PROJECT, \
    NS_FILE_GROUP_TYPE_COMPANY, FileDownloadRecord

from util.jsonresult import getResult

from util.loginrequired import check_request_parmes


def get_bucket_by_group_type(type):
    """
    根据类型获取存储空间
    :param type:
    :return:
    """
    if type == "sys":
        return QN_PUBLIC_BUCKET
    elif type == "user":
        return QN_PUBLIC_BUCKET
    elif type == "project":
        return QN_PRIVATE_BUCKET
    elif type == "company":
        return QN_PUBLIC_BUCKET
    return None


@check_request_parmes(group_type=("group_type", "r"), filetype=("文件类型", "r"), filename=("文件名称", "r"))
@transaction.atomic()
def get_upload_files_url(request):
    """
    获取上传地址
    by: 范俊伟 at:2015-08-28
    修改上传
    by: 范俊伟 at:2015-08-28
    判断用户类型
    by: 范俊伟 at:2015-08-28
    设置文件类型组
    by: 范俊伟 at:2015-08-28
    文件类型处理
    by: 范俊伟 at:2015-08-28
    :param request:
    :return:
    """
    group_type = request.REQUEST.get('group_type')
    bucket = get_bucket_by_group_type(group_type)
    if bucket == None:
        return getResult(False, '无效的group_type')
    fileobj = NsFile()
    if type == "sys":
        fileobj.group_type = NS_FILE_GROUP_TYPE_SYS
    elif type == "user":
        fileobj.group_type = NS_FILE_GROUP_TYPE_USER
    elif type == "project":
        fileobj.group_type = NS_FILE_GROUP_TYPE_PROJECT
    elif type == "company":
        fileobj.group_type = NS_FILE_GROUP_TYPE_COMPANY
    if isinstance(request.user, NSUser):
        fileobj.user = request.user
    fileobj.bucket = bucket
    fileobj.file_status = False
    fileobj.filetype = request.REQUEST.get('filetype').lower().replace(".", "")
    fileobj.name = request.REQUEST.get('filename', '')[-50:]
    uuidname = str(uuid.uuid1())
    object_name = str('%s/%s.%s' % (group_type, uuidname, fileobj.filetype))
    fileobj.fileurl = object_name
    fileobj.save()
    return getResult(True, u'',
                     {'fileid': fileobj.pk, 'posturl': fileobj.get_qn_post_url(), 'params': fileobj.get_qn_params()})


@check_request_parmes(fileid=("文件ID", "r"))
def check_file_upload_status(request):
    """
    判断文件上传是否成功
    by:王健 at:2015-1-26
    :param request:
    :param project_id:
    :return:
    """
    fileurl = request.REQUEST.get('fileid')
    fileobj = get_object_or_404(NsFile, pk=fileurl)
    # todo:获取bcs端 文件是否存在
    return getResult(True, u'', fileobj.check_file())


def get_qn_fop(request, filetype):
    """
    将请求参数转换为七牛云存储数据处理
    by: 范俊伟 at:2015-04-08
    增加文件类型参数
    by: 范俊伟 at:2015-10-09
    :param request:
    :return:
    """
    img_w = request.REQUEST.get('img_w')
    img_h = request.REQUEST.get('img_h')
    if filetype != 'bmp' and filetype != 'jpg' and filetype != 'png' and filetype != 'gif':
        img_h = None
        img_w = None
    fop_args = []
    if img_w and img_h:
        fop_args.append('imageView2/5/w/%s/h/%s' % (img_w, img_h))
    fop = '|'.join(fop_args)
    return fop


@check_request_parmes(fileid=("文件ID", "r"))
def get_file_url(request):
    """
    获取文件下载地址
    by: 范俊伟 at:2015-08-28
    增加文件类型参数
    by: 范俊伟 at:2015-10-09
    返回云盘id
    by: 范俊伟 at:2015-10-31
    纪录下载
    by: 范俊伟 at:2015-10-31
    返回缩略图
    by: 范俊伟 at:2016-02-18
    返回缩略图逻辑修改
    by: 范俊伟 at:2016-02-18
    :param request:
    :param project_id:
    :return:
    """
    mul = request.REQUEST.get('mul') == '1'
    file_ids = [x for x in request.REQUEST.get('fileid', '').strip(',').split(',') if x]
    try:
        for i in file_ids:
            int(i)
    except:
        return getResult(False, 'fileid格式错误')

    fileobjs = NsFile.objects.filter(pk__in=file_ids)
    l = []
    for fileobj in fileobjs:
        if (fileobj.cloud_disk_id or fileobj.group_type == NS_FILE_GROUP_TYPE_PROJECT) and not request.user.is_active:
            raise Http404()

        if request.user.is_active:
            record = FileDownloadRecord()
            record.user = request.user
            record.nsfile = fileobj
            record.save()
        item = fileobj.toJSON()
        item["geturl"] = fileobj.get_url(get_qn_fop(request, fileobj.filetype))
        item["thumbnail"] = fileobj.get_thumbnail()
        l.append(item)
    if len(file_ids) > 1 or mul:
        return getResult(True, u'', l)
    elif len(file_ids) == 1:
        if l:
            return getResult(True, u'', l[0])
    raise Http404()


@check_request_parmes(fileid=("文件ID", "r"))
def upload_complete(request):
    """
    上传完成
    :param request:
    :return:
    """
    file_ids = [x for x in request.REQUEST.get('fileid', '').strip(',').split(',') if x]
    try:
        for i in file_ids:
            int(i)
    except:
        return getResult(False, 'fileid格式错误')

    for id in file_ids:
        NsFile.update_file_status(id)
    return getResult(True, '')
