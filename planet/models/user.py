# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, create_engine, Integer, String, Text, Float, Boolean, orm, DateTime, DECIMAL

from planet.common.base_model import Base


class User(Base):
    """
    用户表
    """
    __tablename__ = "User"
    USid = Column(String(64), primary_key=True)
    USname = Column(String(255), nullable=False, comment='用户名')
    USrealname = Column(String(255), comment='用户真实姓名')
    UStelphone = Column(String(13), nullable=False, comment='手机号')
    USgender = Column(Integer, default=0, comment='性别 {0: man, 1: woman')
    USbirthday = Column(DateTime, comment='出生日期')
    USidentification = Column(String(24), comment='身份证号')
    USheader = Column(Text, default='用户头像')
    USopenid1 = Column(Text, comment='公众号1 openid')
    USopenid2 = Column(Text, comment='公众号2 openid')
    USsupper1 = Column(String(64), comment='一级代理商id')  # 如果一级代理商为空，表示该用户为平台用户
    USsupper2 = Column(String(64), comment='二级代理商id')  # 如果二级代理商为空，则佣金抽成全归一级
    USCommission = Column(Float, comment='佣金分成')        # 总体佣金分成比例
    USintegral = Column(Integer, comment='积分')
    USlevel = Column(Integer, default=1, comment='等级 {1：普通游客，2：代理商}')


class UserLoginTime(Base):
    __tablename__ = 'UserLoginTime'
    ULTid = Column(String(64), primary_key=True)
    USid = Column(String(64), nullable=False, comment='用户id')
    USTcreatetime = Column(DateTime, default=datetime.now(), comment='登录时间')
    USTip = Column(String(64), comment='登录ip地址')


class UserCommission(Base):
    __tablename__ = 'UserCommission'
    UCid = Column(String(64), primary_key=True)
    OMid = Column(String(64), comment='佣金来源订单')
    UCcommission = Column(DECIMAL, comment='获取佣金')
    USid = Column(String(64), comment='用户id')
    UCstatus = Column(Integer, default=0, comment='佣金状态{0：预期到账, 1: 已到账, 2: 已提现}')
    UCcreateTime = Column(DateTime, default=datetime.now(), comment='佣金创建时间')