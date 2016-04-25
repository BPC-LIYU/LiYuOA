# coding=utf-8
from liyu_organization.models import Permissions
from util.jsonresult import get_result
from util.loginrequired import client_login_required


def app_power_permissions(app_flag, org_id, role=['user'], message=u'您不具有使用权限,请联系管理员进行授权'):
    def user_permissions(func=None):
        """

        by:王健 at:2016-04-19
        :param func:
        :return:
        """

        @client_login_required
        def test(request, *args, **kwargs):
            if not isinstance(role, (list, tuple)):
                raise Exception(u'app_power_permissions 的 role 必须是 列表或元组')
            permissions_data = request.session['permissions_data']
            if permissions_data is None:
                permissions_data = {}
                for permission in Permissions.objects.filter(person__user=request.user, is_active=True,
                                                             person__is_active=True, org_id=org_id,
                                                             app__is_active=True, role__is_active=True).select_related('app', 'role'):
                    if not permissions_data.has_key(permission.org_id):
                        permissions_data[permission.org_id] = {}
                    if not permissions_data[permission.org_id].has_key(permission.app.flag):
                        permissions_data[permission.org_id][permission.app.flag] = []
                    permissions_data[permission.org_id][permission.app.flag].append(permission.role.role)
                request.session['permissions_data'] = permissions_data
                request.session.save()
            current_org_id = int(org_id)
            if permissions_data.has_key(current_org_id) and permissions_data[current_org_id].has_key(app_flag):
                    for role_item in role:
                        if role_item in permissions_data[current_org_id][app_flag]:
                            return func(request, *args, **kwargs)
            return get_result(False, message, status_code=8)

        return test

    return user_permissions
