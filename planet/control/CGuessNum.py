# -*- coding: utf-8 -*-
import json
import uuid
from datetime import datetime, date, timedelta

from flask import request, current_app
from sqlalchemy import cast, Date, extract

from planet.common.error_response import StatusError, ParamsError, NotFound, AuthorityError
from planet.common.params_validates import parameter_required
from planet.common.success_response import Success
from planet.common.token_handler import token_required, get_current_user, is_supplizer, is_admin
from planet.control.BaseControl import BASEAPPROVAL
from planet.extensions.register_ext import db
from planet.extensions.validates.activty import GuessNumCreateForm, GuessNumGetForm, GuessNumHistoryForm
from planet.models import GuessNum, CorrectNum, ProductSku, ProductItems, GuessAwardFlow, Products, ProductBrand, \
    UserAddress, AddressArea, AddressCity, AddressProvince, OrderMain, OrderPart, OrderPay, GuessNumAwardApply, \
    ProductSkuValue, ProductImage, Approval, Supplizer, Admin, OutStock
from planet.config.enums import ActivityRecvStatus, OrderFrom, Client, PayType, ProductStatus, GuessNumAwardStatus, \
    ApprovalType, ApplyStatus, ApplyFrom
from planet.extensions.register_ext import alipay, wx_pay
from .COrder import COrder


class CGuessNum(COrder, BASEAPPROVAL):

    @token_required
    def creat(self):
        """参与活动"""
        date_now = datetime.now()
        if date_now.hour > 15:
            raise StatusError('15点以后不开放')
        if date_now.weekday() in [0, 6]:
            raise StatusError('周六周日不开放')
        form = GuessNumCreateForm().valid_data()
        gnnum = form.gnnum.data
        usid = request.user.id

        # if date_now.hour > 15:  # 15点以后参与次日的
        #     gndate = date.today() + timedelta(days=1)
        # else:
        #     gndate = date.today()

        with db.auto_commit():
            today = date.today()

            today_raward = GuessNumAwardApply.query.filter_by_().filter_(
                GuessNumAwardApply.AgreeStartime <= today,
                GuessNumAwardApply.AgreeEndtime >= today,
                GuessNumAwardApply.GNAAstatus == ApplyStatus.agree.value,
            ).first_('今日活动不开放')

            guess_instance = GuessNum.create({
                'GNid': str(uuid.uuid1()),
                'GNnum': gnnum,
                'USid': usid,
                'PRid': today_raward.PRid,
                'SKUid': today_raward.SKUid,
                'Price': today_raward.SKUprice,
                'GNNAid': today_raward.GNAAid
                # 'GNdate': gndate
            })
            db.session.add(guess_instance)
        return Success('参与成功')

    @token_required
    def get(self):
        """获得单日个人参与"""
        form = GuessNumGetForm().valid_data()
        usid = request.user.id
        join_history = GuessNum.query.filter_(
            GuessNum.USid == usid,
            cast(GuessNum.createtime, Date) == form.date.data.date(),
            GuessNum.isdelete == False
        ).first_()
        if not join_history:
            if form.date.data.date() == date.today():
                return Success('今日未参与')
            elif form.date.data.date() == date.today() - timedelta(days=1):
                raise NotFound('昨日未参与')
            else:
                raise NotFound('未参与')
        if join_history:
            # todo 换一种查询方式, 不使用日期筛选, 而使用gnnaid筛选
            correct_num = CorrectNum.query.filter(
                CorrectNum.CNdate == join_history.GNdate
            ).first()
            join_history.fill('correct_num', correct_num)
            if not correct_num:
                result = 'not_open'
            else:
                correct_num.hide('CNid')
                if correct_num.CNnum.strip('0') == join_history.GNnum.strip('0'):
                    result = 'correct'
                else:
                    result = 'uncorrect'
            join_history.fill('result', result).hide('USid', 'PRid')

            product = Products.query.filter_by_({'PRid': join_history.PRid}).first()
            product.fields = ['PRid', 'PRmainpic', 'PRtitle']
            join_history.fill('product', product)
        return Success(data=join_history)

    @token_required
    def history_join(self):
        """获取历史参与记录"""
        form = GuessNumHistoryForm().valid_data()
        year = form.year.data
        month = form.month.data
        try:
            year_month = datetime.strptime(year + '-' + month,  '%Y-%m')
        except ValueError as e:
            raise ParamsError('时间参数异常')
        usid = request.user.id
        join_historys = GuessNum.query.filter(
            extract('month', GuessNum.GNdate) == year_month.month,
            extract('year', GuessNum.GNdate) == year_month.year,
            GuessNum.USid == usid
        ).order_by(GuessNum.GNdate.desc()).group_by(GuessNum.GNdate).all()
        correct_count = 0  # 猜对次数
        for join_history in join_historys:
            correct_num = CorrectNum.query.filter(
                CorrectNum.CNdate == join_history.GNdate
            ).first()
            join_history.fill('correct_num', correct_num)
            if not correct_num:
                result = 'not_open'
            else:
                correct_num.hide('CNid')
                if correct_num.CNnum.strip('0') == join_history.GNnum.strip('0'):
                    result = 'correct'
                    correct_count += 1
                else:
                    result = 'uncorrect'
            join_history.fill('result', result).hide('USid', 'PRid')

            product = Products.query.filter_by_({'PRid': join_history.PRid}).first()
            product.fields = ['PRid', 'PRmainpic', 'PRtitle']
            join_history.fill('product', product)
        return Success(data=join_historys).get_body(correct_count=correct_count)

    @token_required
    def recv_award(self):
        data = parameter_required(('gnid', 'skuid', 'omclient', 'uaid', 'opaytype'))
        gnid = data.get('gnid')
        skuid = data.get('skuid')
        usid = request.user.id
        uaid = data.get('uaid')
        opaytype = data.get('opaytype')
        try:
            omclient = int(data.get('omclient', Client.wechat.value))  # 下单设备
            Client(omclient)
        except Exception as e:
            raise ParamsError('客户端或商品来源错误')

        with db.auto_commit():
            s_list = []
            # 参与记录
            guess_num = GuessNum.query.filter_by_().filter_by_({
                'SKUid': skuid,
                'USid': usid,
                'GNid': gnid
            }).first_('未参与')
            guess_num_apply = GuessNumAwardApply.query.filter(
                GuessNumAwardApply.isdelete == False,
                GuessNumAwardApply.GNAAstatus == ApplyStatus.agree.value,
                GuessNumAwardApply.AgreeStartime <= guess_num.GNdate,
                GuessNumAwardApply.AgreeEndtime >= guess_num.GNdate,
            ).first()
            out_stock = OutStock.query.filter(OutStock.OSid == guess_num_apply.OSid
                                              ).first()
            if out_stock.OSnum is not None:
                out_stock.OSnum = out_stock.OSnum - 1
                if out_stock.OSnum < 0:
                    raise StatusError('库存不足, 活动结束')
                db.session.flush()
            # if guess_num_apply.SKUstock is not None:
            #     guess_num_apply.SKUstock -= 1
            #     if guess_num_apply.SKUstock < 0:
            #         raise StatusError('库存不足, 活动结束')
            #     s_list.append(guess_num_apply)
            price = guess_num.Price
            suid = guess_num_apply.SUid if guess_num_apply.GNAAfrom else None
            # 领奖流水
            guess_award_flow_instance = GuessAwardFlow.query.filter_by_({
                'GNid': gnid,
                'GAFstatus': ActivityRecvStatus.wait_recv.value,
            }).first_('未中奖或已领奖')
            sku_instance = ProductSku.query.filter_by_({"SKUid": skuid}).first_('sku: {}不存在'.format(skuid))
            product_instance = Products.query.filter_by_({"PRid": sku_instance.PRid}).first_('商品已下架')
            pbid = product_instance.PBid
            product_brand_instance = ProductBrand.query.filter_by({'PBid': pbid}).first_()
            # 领奖状态改变
            guess_award_flow_instance.GAFstatus = ActivityRecvStatus.ready_recv.value
            omid = str(uuid.uuid1())
            guess_award_flow_instance.OMid = omid
            s_list.append(guess_award_flow_instance)
            # 用户的地址信息
            user_address_instance = UserAddress.query.filter_by_({'UAid': uaid, 'USid': usid}).first_('地址信息不存在')
            omrecvphone = user_address_instance.UAphone
            areaid = user_address_instance.AAid
            # 地址拼接
            area, city, province = db.session.query(AddressArea, AddressCity, AddressProvince).filter(
                AddressArea.ACid == AddressCity.ACid, AddressCity.APid == AddressProvince.APid).filter(
                AddressArea.AAid == areaid).first_('地址有误')
            address = getattr(province, "APname", '') + getattr(city, "ACname", '') + getattr(
                area, "AAname", '')
            omrecvaddress = address + user_address_instance.UAtext
            omrecvname = user_address_instance.UAname

            # 创建订单
            opayno = self.wx_pay.nonce_str
            # 主单
            order_main_dict = {
                'OMid': omid,
                'OMno': self._generic_omno(),
                'OPayno': opayno,
                'USid': usid,
                'OMfrom': OrderFrom.guess_num_award.value,
                'PBname': product_brand_instance.PBname,
                'PBid': pbid,
                'OMclient': omclient,
                'OMfreight': 0,  # 运费暂时为0
                'OMmount': price,
                'OMmessage': data.get('ommessage'),
                'OMtrueMount': price,
                # 收货信息
                'OMrecvPhone': omrecvphone,
                'OMrecvName': omrecvname,
                'OMrecvAddress': omrecvaddress,
                'PRcreateId': suid
            }
            order_main_instance = OrderMain.create(order_main_dict)
            s_list.append(order_main_instance)
            user = get_current_user()
            order_part_dict = {
                'OMid': omid,
                'OPid': str(uuid.uuid1()),
                'SKUid': skuid,
                'PRattribute': product_instance.PRattribute,
                'SKUattriteDetail': sku_instance.SKUattriteDetail,
                'PRtitle': product_instance.PRtitle,
                'SKUprice': sku_instance.SKUprice,
                'PRmainpic': product_instance.PRmainpic,
                'OPnum': 1,
                'PRid': product_instance.PRid,
                'OPsubTotal': price,
                # 副单商品来源
                'PRfrom': product_instance.PRfrom,
                'PRcreateId': product_instance.CreaterId,
                'UPperid': user.USsupper1,
                'UPperid2': user.USsupper2,
                # todo 活动佣金设置
            }
            order_part_instance = OrderPart.create(order_part_dict)
            s_list.append(order_part_instance)
            # 支付数据表
            order_pay_dict = {
                'OPayid': str(uuid.uuid1()),
                'OPayno': opayno,
                'OPayType': opaytype,
                'OPayMount': price,
            }
            order_pay_instance = OrderPay.create(order_pay_dict)
            s_list.append(order_pay_instance)
            db.session.add_all(s_list)
        # 生成支付信息
        body = product_instance.PRtitle
        user = get_current_user()
        openid = user.USopenid1 or user.USopenid2
        pay_args = self._pay_detail(omclient, opaytype, opayno, float(price), body, openid=openid)
        response = {
            'pay_type': PayType(opaytype).name,
            'opaytype': opaytype,
            'args': pay_args
        }
        return Success('创建订单成功', data=response)

    def list(self):
        """查看自己的申请列表"""
        if is_supplizer():
            suid = request.user.id
        elif is_admin():
            suid = None
        else:
            raise AuthorityError()
        data = parameter_required()
        gnaastatus = data.get('gnaastatus', 'all')
        if str(gnaastatus) == 'all':
            gnaastatus = None
        else:
            gnaastatus = getattr(ApplyStatus, gnaastatus).value
        starttime, endtime = data.get('starttime', '2019-01-01'), data.get('endtime', '2100-01-01')
        out_stocks_query = OutStock.query.join(GuessNumAwardApply, GuessNumAwardApply.OSid == OutStock.OSid
                                               ).group_by(OutStock.OSid).order_by(GuessNumAwardApply.GNAAstarttime.desc(),
                                                                                  GuessNumAwardApply.createtime.desc())
        if suid:
            out_stocks_query = out_stocks_query.filter(GuessNumAwardApply.SUid == suid)
        out_stocks = out_stocks_query.all()
        award_list = list()
        for out_stock in out_stocks:
            awards = GuessNumAwardApply.query.filter(GuessNumAwardApply.isdelete == False,
                                                     GuessNumAwardApply.OSid == out_stock.OSid
                                                     ).filter_(GuessNumAwardApply.GNAAstatus == gnaastatus,
                                                               GuessNumAwardApply.GNAAstarttime >= starttime,
                                                               GuessNumAwardApply.GNAAstarttime <= endtime
                                                               ).all()
            for award in awards:
                award.fill('skustock', out_stock.OSnum)
            award_list.extend(awards)

        for award in award_list:
            sku = ProductSku.query.filter_by(SKUid=award.SKUid).first()
            award.fill('skupic', sku['SKUpic'])
            product = Products.query.filter_by(PRid=award.PRid).first()
            award.fill('prtitle', product.PRtitle)
            award.fill('prmainpic', product['PRmainpic'])
            brand = ProductBrand.query.filter_by(PBid=product.PBid).first()
            award.fill('pbname', brand.PBname)
            award.fill('gnaastatus_zh', ApplyStatus(award.GNAAstatus).zh_value)
            if award.GNAAfrom == ApplyFrom.supplizer.value:
                sup = Supplizer.query.filter_by(SUid=award.SUid).first()
                name = getattr(sup, 'SUname', '')
            elif award.GNAAfrom == ApplyFrom.platform.value:
                admin = Admin.query.filter_by(ADid=award.SUid).first()
                name = getattr(admin, 'ADname', '')
            else:
                name = ''
            award.fill('authname', name)
            award.fill('createtime', award.createtime)

        # 筛选后重新分页
        page = int(data.get('page_num', 1)) or 1
        count = int(data.get('page_size', 15)) or 15
        total_count = len(award_list)
        if page < 1:
            page = 1
        total_page = int(total_count / int(count)) or 1
        start = (page - 1) * count
        if start > total_count:
            start = 0
        if total_count / (page * count) < 0:
            ad_return_list = award_list[start:]
        else:
            ad_return_list = award_list[start: (page * count)]
        request.page_all = total_page
        request.mount = total_count
        return Success(data=ad_return_list)

    def apply_award(self):
        """申请添加奖品"""
        if not (is_supplizer() or is_admin()):
            raise AuthorityError()
        data = parameter_required(('skuid', 'prid', 'gnaastarttime', 'skuprice'))
        skuid, prid, skustock = data.get('skuid'), data.get('prid'), data.get('skustock', 1)
        gnaafrom = ApplyFrom.supplizer.value if is_supplizer() else ApplyFrom.platform.value
        sku = ProductSku.query.filter_by_(SKUid=skuid).first_('没有该skuid信息')
        product = Products.query.filter(Products.PRid == prid, Products.isdelete == False,
                              Products.PRstatus == ProductStatus.usual.value
                              ).first_('当前商品状态不允许进行申请')
        assert sku.PRid == prid, 'sku与商品信息不对应'

        time_list = data.get('gnaastarttime')
        if not isinstance(time_list, list):
            raise ParamsError('参数 gnaastarttime 格式错误')

        # 将申请事物时间分割成每天单位
        # begin_time = str(data.get('gnaastarttime'))[:10]
        # end_time = str(data.get('gnaaendtime'))[:10]
        # time_list = self._getBetweenDay(begin_time, end_time)

        award_instance_list = list()
        gnaaid_list = list()
        skustock = int(skustock)
        with db.auto_commit():
            # 活动出库单
            osid = str(uuid.uuid1())
            db.session.add(OutStock.create({
                'OSid': osid,
                'SKUid': skuid,
                'OSnum': skustock
            }))
            super(CGuessNum, self)._update_stock(-skustock, skuid=skuid)
            for day in time_list:
                # 先检测是否存在相同skuid，相同日期的申请
                exist_apply_sku = GuessNumAwardApply.query.filter(GuessNumAwardApply.SKUid == skuid,
                                                                  GuessNumAwardApply.isdelete == False,
                                                                  GuessNumAwardApply.SUid == request.user.id,
                                                                  GuessNumAwardApply.GNAAstarttime == day).first()
                if exist_apply_sku:
                    raise ParamsError('您已添加过{}日的申请'.format(day))
                award_dict = {
                    'GNAAid': str(uuid.uuid1()),
                    'SUid': request.user.id,
                    'SKUid': skuid,
                    'PRid': prid,
                    'GNAAstarttime': day,
                    'GNAAendtime': day,
                    'SKUprice': float(data.get('skuprice', 0.01)),
                    # 'SKUstock': int(skustock),
                    'OSid': osid,
                    'GNAAstatus': ApplyStatus.wait_check.value,
                    'GNAAfrom': gnaafrom,
                }
                award_instance = GuessNumAwardApply.create(award_dict)
                gnaaid_list.append(award_dict['GNAAid'])
                award_instance_list.append(award_instance)
                # sku.SKUstock -= skustock
                # # 库存设置
                # product.PRstocks -= skustock
                # if sku.SKUstock < 0:
                #     raise StatusError('商品库存不足')
                # db.session.add(sku)
                # if product.PRstocks == 0:
                #     product.PRstatus = ProductStatus.sell_out.value
                # db.session.add(product)
            db.session.add_all(award_instance_list)
        # 添加到审批流
        for gnaaid in gnaaid_list:
            super(CGuessNum, self).create_approval('toguessnum', request.user.id, gnaaid, gnaafrom)
        return Success('申请添加成功', {'gnaaid': gnaaid_list})

    def update_apply(self):
        """修改猜数字奖品申请"""
        if not (is_supplizer() or is_admin()):
            raise AuthorityError()
        data = parameter_required(('gnaaid', 'skuprice', 'skustock'))
        gnaaid, skuid, prid, skustock = data.get('gnaaid'), data.get('skuid'), data.get('prid'), data.get('skustock')
        apply_info = GuessNumAwardApply.query.filter(GuessNumAwardApply.GNAAid == gnaaid,
                                                     GuessNumAwardApply.GNAAstatus.in_([ApplyStatus.reject.value,
                                                                                       ApplyStatus.cancle.value])
                                                     ).first_('只有已拒绝或撤销状态的申请可以进行修改')
        if apply_info.SUid != request.user.id:
            raise AuthorityError('仅可修改自己提交的申请')
        gnaafrom = ApplyFrom.supplizer.value if is_supplizer() else ApplyFrom.platform.value
        sku = ProductSku.query.filter_by_(SKUid=skuid).first_('没有该skuid信息')
        Products.query.filter(Products.PRid == prid, Products.isdelete == False,
                              Products.PRstatus == ProductStatus.usual.value
                              ).first_('仅可将已上架的商品用于申请')  # 当前商品状态不允许进行申请
        assert sku.PRid == prid, 'sku与商品信息不对应'

        other_apply_info = GuessNumAwardApply.query.filter(GuessNumAwardApply.isdelete == False,
                                                           GuessNumAwardApply.GNAAid != gnaaid,
                                                           GuessNumAwardApply.GNAAstatus.notin_(
                                                               [ApplyStatus.cancle.value,
                                                                ApplyStatus.reject.value]),
                                                           GuessNumAwardApply.OSid == apply_info.OSid,
                                                           ).first()
        current_app.logger.info("其他的同批次共用库存申请 --> {}".format(other_apply_info))
        with db.auto_commit():
            award_dict = {
                'SKUid': skuid,
                'PRid': prid,
                'GNAAstarttime': data.get('gnaastarttime'),
                'GNAAendtime': data.get('gnaastarttime'),
                'SKUprice': float(data.get('skuprice', 0.01)),
                # 'SKUstock': int(skustock),
                'GNAAstatus': ApplyStatus.wait_check.value,
                'GNAAfrom': gnaafrom,
            }
            award_dict = {k: v for k, v in award_dict.items() if v is not None}
            GuessNumAwardApply.query.filter_by_(GNAAid=gnaaid).update(award_dict)
            # 是否修改库存
            if not other_apply_info:
                # 如果没有同批正在上架或审核中的，将库存从商品中重新减出来
                out_stock = OutStock.query.filter(OutStock.isdelete == False, OutStock.OSid == apply_info.OSid
                                                  ).first()
                super(CGuessNum, self)._update_stock(-out_stock.OSnum, skuid=apply_info.SKUid)
        # 重新添加到审批流
        super(CGuessNum, self).create_approval('toguessnum', request.user.id, gnaaid, gnaafrom)

        return Success('修改成功', {'gnaaid': gnaaid})

    def award_detail(self):
        """查看申请详情"""
        if not (is_supplizer() or is_admin()):
            args = parameter_required(('gnaaid',))
            gnaaid = args.get('gnaaid')
            award = GuessNumAwardApply.query.filter_by_(GNAAid=gnaaid).first_('该申请已被删除')
            product = Products.query.filter_by_(PRid=award.PRid).first_('商品已下架')
            product.PRattribute = json.loads(product.PRattribute)
            product.PRremarks = json.loads(getattr(product, 'PRremarks') or '{}')
            # 顶部图
            images = ProductImage.query.filter_by_(PRid=product.PRid).order_by(ProductImage.PIsort).all()
            product.fill('images', images)
            # 品牌
            brand = ProductBrand.query.filter_by_(PBid=product.PBid).first() or {}
            product.fill('brand', brand)
            sku = ProductSku.query.filter_by_(SKUid=award.SKUid).first_('没有该skuid信息')
            sku.SKUattriteDetail = json.loads(sku.SKUattriteDetail)
            if sku.SKUstock:
                sku.hide('SKUstock')
            product.fill('sku', sku)
            # # sku value
            # 是否有skuvalue, 如果没有则自行组装
            sku_value_item_reverse = []
            for index, name in enumerate(product.PRattribute):
                value = sku.SKUattriteDetail[index]
                temp = {
                    'name': name,
                    'value': value
                }
                sku_value_item_reverse.append(temp)
            product.fill('skuvalue', sku_value_item_reverse)
            award.fill('product', product)
            return Success('获取成功', award)

    def shelf_award(self):
        """撤销申请"""
        if not (is_supplizer() or is_admin()):
            raise AuthorityError()
        data = parameter_required(('gnaaid',))
        gnaaid = data.get('gnaaid')
        with db.auto_commit():
            apply_info = GuessNumAwardApply.query.filter_by_(GNAAid=gnaaid).first_('无此申请记录')
            other_apply_info = GuessNumAwardApply.query.filter(GuessNumAwardApply.isdelete == False,
                                                               GuessNumAwardApply.GNAAid != gnaaid,
                                                               GuessNumAwardApply.GNAAstatus.notin_(
                                                                   [ApplyStatus.cancle.value,
                                                                    ApplyStatus.reject.value]),
                                                               GuessNumAwardApply.OSid == apply_info.OSid,
                                                               ).first()
            current_app.logger.info("其他的同库存申请 --> {}".format(other_apply_info))
            if apply_info.GNAAstatus != ApplyStatus.wait_check.value:
                raise StatusError('只有在审核状态的申请可以撤销')
            if apply_info.SUid != request.user.id:
                raise AuthorityError('仅可撤销自己提交的申请')
            apply_info.GNAAstatus = ApplyStatus.cancle.value
            # 是否修改库存
            if not other_apply_info:
                out_stock = OutStock.query.filter(OutStock.isdelete == False, OutStock.OSid == apply_info.OSid
                                                  ).first()
                super(CGuessNum, self)._update_stock(out_stock.OSnum, skuid=apply_info.SKUid)
            # 同时将正在进行的审批流改为取消
            approval_info = Approval.query.filter_by_(AVcontent=gnaaid, AVstartid=request.user.id,
                                                      AVstatus=ApplyStatus.wait_check.value).first()
            approval_info.AVstatus = ApplyStatus.cancle.value
        return Success('取消成功', {'gnaaid': gnaaid})

    def delete_apply(self):
        """删除申请"""
        if is_supplizer():
            usid = request.user.id
            sup = Supplizer.query.filter_by_(SUid=usid).first_('供应商信息错误')
            current_app.logger.info('Supplizer {} delete guessnum apply'.format(sup.SUname))
        elif is_admin():
            usid = request.user.id
            admin = Admin.query.filter_by_(ADid=usid).first_('管理员信息错误')
            current_app.logger.info('Admin {} guessnum apply'.format(admin.ADname))
            sup = None
        else:
            raise AuthorityError()
        data = parameter_required(('gnaaid',))
        gnaaid = data.get('gnaaid')
        with db.auto_commit():
            apply_info = GuessNumAwardApply.query.filter_by_(GNAAid=gnaaid).first_('无此申请记录')
            if sup:
                assert apply_info.SUid == usid, '供应商只能删除自己提交的申请'
            if apply_info.GNAAstatus not in [ApplyStatus.cancle.value, ApplyStatus.reject.value]:
                raise StatusError('只能删除已拒绝或已撤销状态下的申请')
            apply_info.isdelete = True
        return Success('删除成功', {'gnaaid': gnaaid})

    def shelves(self):
        """下架申请"""
        if is_supplizer():
            usid = request.user.id
            sup = Supplizer.query.filter_by_(SUid=usid).first_('供应商信息错误')
            current_app.logger.info('Supplizer {} delete guessnum apply'.format(sup.SUname))
        elif is_admin():
            usid = request.user.id
            admin = Admin.query.filter_by_(ADid=usid).first_('管理员信息错误')
            current_app.logger.info('Admin {} guessnum apply'.format(admin.ADname))
            sup = None
        else:
            raise AuthorityError()
        data = parameter_required(('gnaaid',))
        gnaaid = data.get('gnaaid')
        with db.auto_commit():
            apply_info = GuessNumAwardApply.query.filter_by_(GNAAid=gnaaid).first_('无此申请记录')
            if sup:
                assert apply_info.SUid == usid, '供应商只能下架自己的申请'
            if apply_info.GNAAstatus != ApplyStatus.agree.value:
                raise StatusError('只能下架已通过的申请')
            apply_info.GNAAstatus = ApplyStatus.reject.value
        return Success('下架成功', {'mbaid': gnaaid})

    @staticmethod
    def _getBetweenDay(begin_date, end_date):
        date_list = []
        begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += timedelta(days=1)
        return date_list
