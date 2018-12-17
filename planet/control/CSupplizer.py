import random
import re
import uuid
import json
from threading import Thread

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from planet.common.Inforsend import SendSMS
from planet.common.error_response import AuthorityError, ParamsError, DumpliError
from planet.common.params_validates import parameter_required
from planet.common.success_response import Success
from planet.common.token_handler import admin_required, is_admin, is_supplizer, token_required
from planet.extensions.register_ext import db, conn
from planet.extensions.validates.user import SupplizerListForm, SupplizerCreateForm, SupplizerGetForm, \
    SupplizerUpdateForm, SupplizerSendCodeForm, SupplizerResetPasswordForm, SupplizerChangePasswordForm
from planet.models import Supplizer


class CSupplizer:
    def __init__(self):
        pass

    @admin_required
    def list(self):
        """供应商列表"""
        form = SupplizerListForm().valid_data()
        kw = form.kw.data
        mobile = form.mobile.data

        supplizers = Supplizer.query.filter_by_().filter_(
            Supplizer.SUname.contains(kw),
            Supplizer.SUlinkPhone.contains(mobile)
        ).all_with_page()
        for supplizer in supplizers:
            supplizer.hide('SUpassword')
        return Success(data=supplizers)

    @admin_required
    def create(self):
        """添加"""
        form = SupplizerCreateForm().valid_data()
        with db.auto_commit():
            supperlizer = Supplizer.create({
                'SUid': str(uuid.uuid1()),
                'SUlinkPhone': form.sulinkphone.data,
                'SUloginPhone': form.suloginphone.data,
                'SUname': form.suname.data,
                'SUlinkman': form.sulinkman.data,
                'SUaddress': form.suaddress.data,
                'SUbanksn': form.subanksn.data,
                'SUbankname': form.subankname.data,
                'SUpassword': generate_password_hash(form.supassword.data),
                'SUheader': form.suheader.data,
                'SUcontract': form.sucontract.data,
            })
            db.session.add(supperlizer)
        return Success('创建成功', data={'suid': supperlizer.SUid})

    def update(self):
        """更新供应商信息"""
        if not is_admin() and not is_supplizer():
            raise AuthorityError()
        form = SupplizerUpdateForm().valid_data()
        with db.auto_commit():
            supplizer = Supplizer.query.filter(
                Supplizer.isdelete == False,
                Supplizer.SUid == form.suid.data
            ).first_('供应商不存在')
            supplizer.update({
                'SUlinkPhone': form.sulinkphone.data,
                'SUloginPhone': form.suloginphone.data,
                'SUname': form.suname.data,
                'SUlinkman': form.sulinkman.data,
                'SUaddress': form.suaddress.data,
                'SUbanksn': form.subanksn.data,
                'SUbankname': form.subankname.data,
                # 'SUpassword': generate_password_hash(form.supassword.data),
                'SUheader': form.suheader.data,
                'SUcontract': form.sucontract.data,
            }, null='dont ignore')
            db.session.add(supplizer)
        return Success('更新成功')

    @token_required
    def get(self):
        if not is_admin() and not is_supplizer():
            raise AuthorityError()
        form = SupplizerGetForm().valid_data()
        supplizer = form.supplizer
        supplizer.hide('SUpassword')
        return Success(data=supplizer)

    @token_required
    def change_password(self):
        if not is_supplizer() and not is_admin():
            raise AuthorityError()
        form = SupplizerChangePasswordForm().valid_data()
        old_password = form.oldpassword.data
        supassword = form.supassword.data
        suid = form.suid.data
        with db.auto_commit():
            supplizer = Supplizer.query.filter(
                Supplizer.isdelete == False,
                Supplizer.SUid == suid
            ).first_('不存在的供应商')
            if not is_admin() and not check_password_hash(supplizer.SUpassword, old_password):
                raise AuthorityError('原密码错误')
            supplizer.SUpassword = generate_password_hash(supassword)
            db.session.add(supplizer)
        return Success('修改成功')



    @token_required
    def reset_password(self):
        form = SupplizerResetPasswordForm().valid_data()
        mobile = form.suloginphone.data
        password = form.supassword.data
        if is_supplizer():
            code = form.code.data
            correct_code = conn.get(mobile + '_code')
            if correct_code:
                correct_code = correct_code.decode()
            current_app.logger.info('correct code is {}, code is {}'.format(correct_code, code))
            if code != correct_code:
                raise ParamsError('验证码错误')
        if not is_admin():
            raise AuthorityError()
        with db.auto_commit():
            Supplizer.query.filter(
                Supplizer.isdelete == False,
                Supplizer.SUloginPhone == mobile
            ).update({
                'SUpassword': generate_password_hash(password)
            })
        return Success('修改成功')

    @token_required
    def send_reset_password_code(self):
        """发送修改验证码"""
        if not is_supplizer():
            raise AuthorityError()
        form = SupplizerSendCodeForm().valid_data()
        mobile = form.suloginphone.data
        Supplizer.query.filter(
            Supplizer.isdelete == False,
            Supplizer.SUloginPhone == mobile
        ).first_('不存在的供应商')
        exist_code = conn.get(mobile + '_code')
        if exist_code:
            return DumpliError('重复发送')
        nums = [str(x) for x in range(10)]
        code = ''.join([random.choice(nums) for _ in range(6)])
        key = mobile + '_code'
        conn.set(key, code, ex=60)  # 60s过期
        params = {"code": code}
        app = current_app._get_current_object()
        send_task = Thread(target=self._async_send_code, args=(mobile, params, app), name='send_code')
        send_task.start()
        return Success('发送成功')

    def _async_send_code(self, mobile, params, app):
        with app.app_context():
            response_send_message = SendSMS(mobile, params)
            if not response_send_message:
                current_app.logger.error('发送失败')






