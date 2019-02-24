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
    ProductSkuValue, ProductImage, Approval, Supplizer, Admin, OutStock, ProductCategory, GuessNumAwardProduct, \
    GuessNumAwardSku
from planet.config.enums import ActivityRecvStatus, OrderFrom, Client, PayType, ProductStatus, GuessNumAwardStatus, \
    ApprovalType, ApplyStatus, ApplyFrom
from planet.extensions.register_ext import alipay, wx_pay
from .COrder import COrder


class CGuessNum(COrder, BASEAPPROVAL):

    @token_required
    def creat(self):
        # todo 修改具体内容
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
        # todo 修改字段
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
        # todo 修改字段
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
        # todo 修改接口为创建订单，增加时间和猜中多少个数字的判断。根据多少个数字获取减免金额。
        data = parameter_required(('prid', 'gnaaendtime', 'gnaastarttime', 'prprice', 'skus'))
        # apply_from = ApplyFrom.supplizer.value if is_supplizer() else

    def list(self):
        # todo 修改字段
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
        data = parameter_required(('prid', 'prprice', 'skus', 'gnaastarttime'))
        gnaafrom = ApplyFrom.supplizer.value if is_supplizer() else ApplyFrom.platform.value
        # 欲申请商品
        product = Products.query.filter_by(
            PRid=data.get('prid'), isdelete=False, PRstatus=ProductStatus.usual.value).first_('商品未上架')
        product_brand = ProductBrand.query.filter_by(PBid=product.PBid).first_('商品信息不全')
        # 时间列表
        time_list = data.get('gnaastarttime')
        # 申请的sku list
        skus = data.get('skus')
        with db.auto_commit():
            # 系统实际生成的申请id列表， 按日期不同生成不同的申请单
            gnaaid_list = list()
            for day in time_list:
                # 校验是否存在已提交申请
                exist_apply = GuessNumAwardApply.query.filter(
                    GuessNumAwardProduct.PRid == data.get('prid'),
                    # GuessNumAwardProduct.GNAPid == GuessNumAwardApply.GNAPid,
                    GuessNumAwardApply.isdelete == False,
                    GuessNumAwardApply.SUid == request.user.id,
                    GuessNumAwardApply.GNAAstarttime == day).first()
                if exist_apply:
                    raise ParamsError('您已添加过{}日的申请'.format(day))
                # 申请单
                gnaa = GuessNumAwardApply.create({
                    'GNAAid': str(uuid.uuid1()),
                    'SUid': request.user.id,
                    # 'GNAPid': data.get('prid'),
                    'GNAAstarttime': day,
                    'GNAAendtime': day,
                    'GNAAfrom': gnaafrom,
                    'GNAAstatus': ApplyStatus.wait_check.value,
                })
                db.session.add(gnaa)
                gnaaid_list.append(gnaa.GNAAid)
                # 活动商品
                gnap = GuessNumAwardProduct.create({
                    'GNAPid': str(uuid.uuid1()),
                    'GNAAid': gnaa.GNAAid,
                    'PRid': product.PRid,
                    'PRmainpic': product.PRmainpic,
                    'PRtitle': product.PRtitle,
                    'PBid': product.PBid,
                    'PBname': product_brand.PBname,
                    'PRattribute': product.PRattribute,
                    'PRdescription': product.PRdescription,
                    'PRprice': data.get('prprice')
                })
                db.session.add(gnap)
                # 活动sku
                for sku in skus:
                    skuid = sku.get('skuid')
                    skuprice = sku.get('skuprice')
                    skustock = sku.get('skustock')
                    skudiscountone = sku.get('skudiscountone')
                    skudiscounttwo = sku.get('skudiscounttwo')
                    skudiscountthree = sku.get('skudiscountthree')
                    skudiscountfour = sku.get('skudiscountfour')
                    skudiscountfive = sku.get('skudiscountfive')
                    skudiscountsix = sku.get('skudiscountsix')
                    sku_instance = ProductSku.query.filter_by(
                        isdelete=False, PRid=product.PRid, SKUid=skuid).first_('商品sku信息不存在')
                    self._update_stock(-int(skustock), product, sku_instance)
                    # db.session.add(sku)
                    gnas = GuessNumAwardSku.create({
                        'GNASid': str(uuid.uuid1()),
                        'GNAPid': gnap.GNAPid,
                        'SKUid': skuid,
                        'SKUprice': skuprice,
                        'SKUdiscountone': skudiscountone,
                        'SKUdiscounttwo': skudiscounttwo,
                        'SKUdiscountthree': skudiscountthree,
                        'SKUdiscountfour': skudiscountfour,
                        'SKUdiscountfive': skudiscountfive,
                        'SKUdiscountsix': skudiscountsix,
                    })
                    db.session.add(gnas)

        # 添加到审批流
        for gnaaid in gnaaid_list:
            super(CGuessNum, self).create_approval('toguessnum', request.user.id, gnaaid, gnaafrom)
        return Success('申请添加成功', {'gnaaid': gnaaid_list})

    def update_apply(self):
        """修改猜数字奖品申请, 一次只能处理一天的一个商品"""
        if not (is_supplizer() or is_admin()):
            raise AuthorityError()
        # data = parameter_required(('gnaaid', 'skuprice', 'skustock'))
        data = parameter_required(('gnaaid', 'prid', 'prprice', 'skus'))
        # 获取申请单
        apply_info = GuessNumAwardApply.query.filter(GuessNumAwardApply.GNAAid == data.get('gnaaid'),
                                                     GuessNumAwardApply.GNAAstatus.in_([ApplyStatus.reject.value,
                                                                                       ApplyStatus.cancle.value])
                                                     ).first_('只有已拒绝或撤销状态的申请可以进行修改')
        if apply_info.SUid != request.user.id:
            raise AuthorityError('仅可修改自己提交的申请')
        gnaafrom = ApplyFrom.supplizer.value if is_supplizer() else ApplyFrom.platform.value
        # 获取原商品属性
        product_old = GuessNumAwardProduct.query.filter(GuessNumAwardProduct.GNAAid == apply_info.GNAAid,
                                                        GuessNumAwardProduct.isdelete == False).first()
        # 获取原sku属性
        gnas_old = GuessNumAwardSku.query.filter(
            apply_info.GNAAid == GuessNumAwardProduct.GNAAid,
            GuessNumAwardSku.GNAPid == GuessNumAwardProduct.GNAPid,
            GuessNumAwardSku.isdelete == False,
            GuessNumAwardProduct.isdelete == False,
        ).all()
        # 解除和原商品属性的绑定
        # GuessNumAwardProduct.query.filter_by(GNAAid=apply_info.GNAAid, PRid=product_old.PRid).delete_()
        product_old.isdelete = True
        # 获取修改后的时间。如果没有修改时间则用原时间
        gnaastarttime = data.get('gnaastarttime') or apply_info.GNAAstarttime
        # 如果修改了时间，检测是否有冲突
        exist_apply_list = list()
        # 遍历原sku 将库存退出去
        for sku in gnas_old:
            sku_instance = ProductSku.query.filter_by(
                isdelete=False, PRid=product_old.PRid, SKUid=sku.SKUid).first_('商品sku信息不存在')
            self._update_stock(int(sku.SKUstock), product_old.PRid, sku_instance)

        # 重新添加商品属性
        skus = data.get('skus')
        product = Products.query.filter_by(
            PRid=data.get('prid'), isdelete=False, PRstatus=ProductStatus.usual.value).first_('商品未上架')
        product_brand = ProductBrand.query.filter_by(PBid=product.PBid).first_('商品信息不全')
        # 新的商品属性
        gnap = GuessNumAwardProduct.create({
            'GNAPid': str(uuid.uuid1()),
            # 'GNAAid': gnaa.GNAAid,
            'PRid': product.PRid,
            'PRmainpic': product.PRmainpic,
            'PRtitle': product.PRtitle,
            'PBid': product.PBid,
            'PBname': product_brand.PBname,
            'PRattribute': product.PRattribute,
            'PRdescription': product.PRdescription,
            'PRprice': data.get('prprice')
        })
        db.session.add(gnap)
        # 新的sku属性
        for sku in skus:
            # 冲突校验。 如果冲突，则跳过，并予以提示
            exits_apply = GuessNumAwardApply.query.filter(
                GuessNumAwardApply.GNAAid != apply_info.GNAAid,
                GuessNumAwardApply.GNAAstarttime == gnaastarttime,
                GuessNumAwardProduct.GNAAid == GuessNumAwardApply.GNAAid,
                GuessNumAwardProduct.PRid == data.get('prid'),
                GuessNumAwardSku.SKUid == sku.SKUid,
                GuessNumAwardSku.GNAPid == GuessNumAwardProduct.GNAPid,
                GuessNumAwardProduct.isdelete == False,
                GuessNumAwardSku.isdelete == False,
                GuessNumAwardApply.isdelete == False
            ).first()

            skuid = sku.get('skuid')
            skuprice = sku.get('skuprice')
            skustock = sku.get('skustock')
            SKUdiscountone = sku.get('SKUdiscountone')
            SKUdiscounttwo = sku.get('SKUdiscounttwo')
            SKUdiscountthree = sku.get('SKUdiscountthree')
            SKUdiscountfour = sku.get('SKUdiscountfour')
            SKUdiscountfive = sku.get('SKUdiscountfive')
            SKUdiscountsix = sku.get('SKUdiscountsix')
            sku_instance = ProductSku.query.filter_by(
                isdelete=False, PRid=product.PRid, SKUid=skuid).first_('商品sku信息不存在')

            if exits_apply:
                exist_apply_list.append(sku_instance)
                continue
            # 库存处理
            self._update_stock(-int(skustock), product, sku_instance)

            gnas = GuessNumAwardSku.create({
                'GNASid': str(uuid.uuid1()),
                'GNAPid': gnap.GNAPid,
                'SKUid': skuid,
                'SKUprice': skuprice,
                'SKUdiscountone': SKUdiscountone,
                'SKUdiscounttwo': SKUdiscounttwo,
                'SKUdiscountthree': SKUdiscountthree,
                'SKUdiscountfour': SKUdiscountfour,
                'SKUdiscountfive': SKUdiscountfive,
                'SKUdiscountsix': SKUdiscountsix,
            })
            db.session.add(gnas)

        super(CGuessNum, self).create_approval('toguessnum', request.user.id, apply_info.GNAAid, gnaafrom)

        return Success('修改成功', {'gnaaid': apply_info.GNAAid, 'skus': exist_apply_list})

    def award_detail(self):
        """查看申请详情"""
        # todo 字段修改
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
