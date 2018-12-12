from flask import request

from planet.common.success_response import Success
from planet.common.token_handler import token_required, usid_to_token
from planet.models import User, Admin


class CAuth:
    @token_required
    def fresh(self):
        usid = request.user.id
        if request.user.model == 'User':
            user = User.query.filter(
                User.USid == usid,
                User.isdelete == False
            ).first_('用户已删除')
            jwt = usid_to_token(usid, model='User', level=user.USlevel)
        elif request.user.model == 'Admin':
            admin = Admin.query.filter(
                Admin.ADid == request.user.id,
                Admin.isdelete == False,
                Admin.ADstatus == 0
            ).first_('管理员状态有误')
            jwt = usid_to_token(usid, model='Admin', level=admin.ADlevel)
        else:
            jwt = None
        return Success(data=jwt)



