# -*- coding: utf-8 -*-
import json
import random
import time
import uuid
from decimal import Decimal

from alipay import AliPay
from flask import request

from planet.common.params_validates import parameter_required
from planet.common.error_response import ParamsError, SystemError
from planet.common.success_response import Success
from planet.common.token_handler import token_required
from planet.config.enums import PayType, Client, OrderFrom, OrderMainStatus, OrderPartStatus
from planet.config.secret import appid, mch_id, mch_key, wxpay_notify_url, alipay_appid, app_private_path, \
    alipay_public_key_path, alipay_notify
from planet.extensions.weixin import WeixinPay
from planet.models import ProductSku, Products, ProductBrand
from planet.models.trade import OrderMain, OrderPart, OrderPay, Carts
from planet.service.STrade import STrade


class COrder:
    def __init__(self):
        self.strade = STrade()

    @token_required
    def list(self):
        usid = request.user.id
        data = parameter_required()
        status = data.get('omstatus')
        order_mains = self.strade.get_ordermain_list({'USid': usid, 'OMstatus': status})
        for order_main in order_mains:
            order_parts = self.strade.get_orderpart_list({'OMid': order_main.OMid})
            for order_part in order_parts:
                order_part.SKUdetail = json.loads(order_part.SKUdetail)
                # 状态
                order_part.OPstatus_en = OrderPartStatus(order_part.OPstatus).name
                order_part.add('OPstatus_en')
            order_main.fill('order_part', order_parts)
            # 状态
            order_main.OMstatus_en = OrderMainStatus(order_main.OMstatus).name
            order_main.add('OMstatus_en').hide('OPayno', 'USid', )
        return Success(data=order_mains)

    @token_required
    def create(self):
        """创建并发起支付"""
        data = parameter_required(('info', 'omclient', 'omfrom', 'udid', 'opaytype'))
        usid = request.user.id
        udid = data.get('udid')  # todo udid 表示用户的地址信息
        opaytype = data.get('opaytype')
        try:
            omclient = int(data.get('omclient', 0))  # 下单设备
            omfrom = int(data.get('omfrom', 0))  # 商品来源
            Client(omclient)
            OrderFrom(omfrom)
        except Exception as e:
            raise ParamsError('客户端或商品来源错误')
        infos = data.get('info')
        with self.strade.auto_commit() as s:
            body = set()  # 付款时候需要使用的字段
            omrecvphone = '18753391801'
            omrecvaddress = '钱江世纪城'
            omrecvname = '老哥'
            opayno = self.wx_pay.nonce_str
            model_bean = []
            mount_price = Decimal()  # 总价
            for info in infos:
                order_price = Decimal()  # 订单价格
                omid = str(uuid.uuid4())  # 主单id
                info = parameter_required(('pbid', 'skus', ), datafrom=info)
                pbid = info.get('pbid')
                skus = info.get('skus')
                ommessage = info.get('ommessage')
                product_brand_instance = s.query(ProductBrand).filter_by_({'PBid': pbid}).first_('品牌id: {}不存在'.format(pbid))
                for sku in skus:
                    # 订单副单
                    opid = str(uuid.uuid4())
                    skuid = sku.get('skuid')
                    opnum = int(sku.get('opnum', 1))
                    assert opnum > 0
                    sku_instance = s.query(ProductSku).filter_by_({'SKUid': skuid}).first_('skuid: {}不存在'.format(skuid))
                    prid = sku_instance.PRid
                    product_instance = s.query(Products).filter_by_({'PRid': prid}).first_('skuid: {}对应的商品不存在'.format(skuid))
                    if product_instance.PBid != pbid:
                        raise ParamsError('品牌id: {}与skuid: {}不对应'.format(pbid, skuid))
                    small_total = Decimal(str(sku_instance.SKUprice)) * opnum
                    order_part_dict = {
                        'OMid': omid,
                        'OPid': opid,
                        'SKUid': skuid,
                        'SKUdetail': sku_instance.SKUdetail,
                        'PRtitle': product_instance.PRtitle,
                        'SKUprice': sku_instance.SKUprice,
                        'PRmainpic': product_instance.PRmainpic,
                        'OPnum': opnum,
                        'PRid': product_instance.PRid,
                        'OPsubTotal': small_total,
                    }
                    order_part_instance = OrderPart.create(order_part_dict)
                    model_bean.append(order_part_instance)
                    # 订单价格计算
                    order_price += small_total
                    # 删除购物车
                    s.query(Carts).filter_by_({"USid": usid, "SKUid": skuid}).delete_()
                    # body 信息
                    body.add(product_instance.PRtitle)
                # 主单
                order_main_dict = {
                    'OMid': omid,
                    'OMno': self._generic_omno(),
                    'OPayno': opayno,
                    'USid': usid,
                    'OMfrom': omfrom,
                    'PBname': product_brand_instance.PBname,
                    'PBid': pbid,
                    'OMclient': omclient,
                    'OMfreight': 0, # 运费暂时为0
                    'OMmount': order_price,
                    'OMmessage': ommessage,
                    'OMtrueMount': order_price,  # 暂时付费不优惠
                    # 收货信息
                    'OMrecvPhone': omrecvphone,
                    'OMrecvName': omrecvname,
                    'OMrecvAddress': omrecvaddress,
                }
                order_main_instance = OrderMain.create(order_main_dict)
                model_bean.append(order_main_instance)
                # 总价格累加
                mount_price += order_price
            # 支付数据表
            order_pay_dict = {
                'OPayid': str(uuid.uuid4()),
                'OPayno': opayno,
                'OPayType': opaytype,
                'OPayMount': mount_price
            }
            order_pay_instance = OrderPay.create(order_pay_dict)
            model_bean.append(order_pay_instance)
            s.add_all(model_bean)
        # 生成支付信息
        body = ''.join(list(body))
        pay_args = self._pay_detail(omclient, opaytype, opayno, float(mount_price), body)
        response = {
            'pay_type': PayType(opaytype).name,
            'opaytype': opaytype,
            'args': pay_args
        }
        return Success('创建成功', data=response)

    @token_required
    def pay(self):
        """订单发起支付"""
        data = parameter_required('omid')
        omid = data.get('omid', 'omclient', 'opaytype')
        try:
            omclient = int(data.get('omclient'))  # 客户端(app或者微信)
            opaytype = int(data.get('opaytype'))  # 付款方式
            PayType(opaytype)
            Client(omclient)
        except Exception as e:
            raise ParamsError('客户端或支付类型错误')
        order_main = self.strade.get_ordermain_one({'OMid': omid}, '不存在的订单')
        with self.strade.auto_commit() as s:
            opayno = self.wx_pay.nonce_str
            # 原支付流水删除
            # 更改订单支付编号
            # 新建支付流水



    def _pay_detail(self, omclient, opaytype, opayno, mount_price, body, openid='openid'):
        if opaytype == PayType.wechat_pay.value:
            body = body[:110] + '...'
            wechat_pay_dict = dict(
                body=body,
                out_trade_no=opayno,
                total_fee=int(mount_price * 100), attach='attach',
                spbill_create_ip=request.remote_addr
            )
            if omclient == Client.wechat.value:  # 微信客户端
                wechat_pay_dict.update(dict(trade_type="JSAPI", openid=openid))
                raw = self.wx_pay.jsapi(**wechat_pay_dict)
            else:
                wechat_pay_dict.update(dict(trade_type="APP"))
                raw = self.wx_pay.unified_order(**wechat_pay_dict)
        elif opaytype == PayType.alipay.value:
            if omclient == Client.wechat.value:
                raise SystemError('请选用其他支付方式')
            else:
                raw = self.alipay.api_alipay_trade_app_pay(
                    out_trade_no=opayno,
                    total_amount=mount_price,
                    subject=body[:200] + '...',
                )
        else:
            raise SystemError('请选用其他支付方式')
        return raw

    @staticmethod
    def _generic_omno():
        """生成订单号"""
        return str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) +\
                 str(time.time()).replace('.', '')[-7:] + str(random.randint(1000, 9999))

    @property
    def wx_pay(self):
        return WeixinPay(appid, mch_id, mch_key, wxpay_notify_url)  # 后两个参数可选

    @property
    def alipay(self):
        return AliPay(
            appid=alipay_appid,
            app_notify_url=alipay_notify,  # 默认回调url
            app_private_key_string=open(app_private_path).read(),
            alipay_public_key_string=open(alipay_public_key_path).read(),
            sign_type="RSA",  # RSA 或者 RSA2
        )