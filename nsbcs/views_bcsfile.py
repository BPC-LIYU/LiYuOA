# coding=utf-8
# Date:2014/7/25
# Email:wangjian2254@gmail.com
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
import uuid
from nsbcs.models import NsFile, NS_FILE_GROUP_TYPE_SYS, NS_FILE_GROUP_TYPE_USER, \
    NS_FILE_GROUP_TYPE_ORG
from util.jsonresult import get_result
from util.loginrequired import check_request_parmes

__author__ = u'王健'


def get_bucket_by_access_type(group_type):
    """
    根据类型获取存储空间
    by:王健 at:2016-04-20
    :param group_type:
    :return:
    """
    if group_type == "public":
        return settings.QN_PUBLIC_BUCKET
    elif group_type == "private":
        return settings.QN_PRIVATE_BUCKET
    return None


@check_request_parmes(access_type=("文件访问类型", "r"), filetype=("文件类型", "r"), filename=("文件名称", "r"))
@transaction.atomic()
def get_upload_files_url(request, access_type, filetype, filename):
    """
    获取上传文件的url信息
    :param filetype:
    :param filename:
    :param access_type:
    :param request:
    :return:
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
    """
    bucket = get_bucket_by_access_type(access_type)
    if bucket is None:
        return get_result(False, '无效的group_type')
    fileobj = NsFile()

    if request.user.is_anonymous():
        fileobj.user = request.user
    fileobj.bucket = bucket
    fileobj.file_status = False
    fileobj.filetype = filetype
    fileobj.name = filename[-20:]
    uuidname = str(uuid.uuid1())
    object_name = str('%s/%s.%s' % (access_type, uuidname, fileobj.filetype))
    fileobj.fileurl = object_name
    fileobj.save()
    return get_result(True, u'',
                      {'fileid': fileobj.pk, 'posturl': fileobj.get_qn_post_url(), 'params': fileobj.get_qn_params()})


def get_qn_fop(img_w, img_h, filetype):
    """
    将请求参数转换为七牛云存储数据处理
    by: 范俊伟 at:2015-04-08
    增加文件类型参数
    by: 范俊伟 at:2015-10-09
    :param filetype:
    :param img_h:
    :param img_w:
    :return:
    """
    if filetype.lower() not in ['bmp', 'jpg', 'jpeg', 'png', 'gif']:
        img_h = None
        img_w = None
    fop_args = []
    if img_w and img_h:
        fop_args.append('imageView2/5/w/%s/h/%s' % (img_w, img_h))
    fop = '|'.join(fop_args)
    return fop


@check_request_parmes(fileid=("文件ID", "r,[int]"), img_w=("图片宽度", "int"), img_h=("图片高度", "int"))
def get_file_url_public(request, fileid, img_w, img_h):
    """
    获取文件url
    by:王健 at:2016-04-20
    :param img_h:
    :param img_w:
    :param fileid:
    :param request:
    :return:
    """
    fileobjs = NsFile.objects.filter(pk__in=fileid, access_type="public").list_json()
    formate_file_url(img_w, img_h, fileobjs)
    return get_result(True, u'', fileobjs)


@check_request_parmes(fileid=("文件ID", "r,[int]"), img_w=("图片宽度", "int"), img_h=("图片高度", "int"))
def get_file_url_private(request, fileid, img_w, img_h):
    """
    获取文件url
    by:王健 at:2016-04-20
    :param img_h:
    :param img_w:
    :param fileid:
    :param request:
    :return:
    """
    fileobjs = NsFile.objects.filter(pk__in=fileid).list_json()
    formate_file_url(img_w, img_h, fileobjs)
    return get_result(True, u'', fileobjs)


def formate_file_url(img_w, img_h, fileobjs):
    """
    格式化文件字典
    by:王健 at:2016-04-20
    :param img_h:
    :param img_w:
    :param fileobjs:
    :return:
    """
    for fileobj in fileobjs:
        fileobj["geturl"] = NsFile.get_url(fileobj['fileurl'], fileobj['bucket'], fileobj['name'],
                                           get_qn_fop(img_w, img_h, fileobj.filetype))
        fileobj["thumbnail"] = NsFile.get_thumbnail(fileobj['fileurl'], fileobj['bucket'], fileobj['name'],
                                                    fileobj['filetype'])


@check_request_parmes(fileid=("文件ID", "r,[int]"), user_id=('用户', 'int'), person_id=('组织成员', 'int'),
                      org_id=('组织', 'int'))
def upload_complete(request, fileid, user_id=None, person_id=None, org_id=None):
    """
    修改文件的is_active 状态
    :param org_id:
    :param person_id:
    :param user_id:
    :param fileid:
    :param request:
    :return:
    """
    for fileobj in NsFile.objects.filter(pk__in=fileid):
        NsFile.update_file_status(fileobj, user_id)
    return get_result(True, '')
