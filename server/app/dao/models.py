from sqlalchemy import Column, Integer, BigInteger, String

from app.dao.database import Base


class App(Base):
    __tablename__ = 'pay_app'
    id = Column(BigInteger, primary_key=True, index=True)
    appname = Column(String, nullable=False, default='')
    pay_appid = Column(String, nullable=False, default='')
    pay_secret_key = Column(String, nullable=False, default='')
    allow_payment = Column(String, nullable=False, default='Y')
    allow_refund = Column(String, nullable=False, default='N')
    create_time = Column(BigInteger, nullable=False, default=0)
    update_time = Column(BigInteger, nullable=False, default=0)
    delete_time = Column(BigInteger, nullable=False, default=0)


class WxMchCfg(Base):
    __tablename__ = 'pay_wx_mch_cfg'
    id = Column(BigInteger, primary_key=True, index=True)
    cfg_name = Column(String, nullable=False, default='')
    mch_id = Column(String, nullable=False, default='')
    mch_v3_key = Column(String, nullable=False, default='')
    mch_pk_path = Column(String, nullable=False, default='')
    mch_serial_no = Column(String, nullable=False, default='')
    create_time = Column(BigInteger, nullable=False, default=0)
    update_time = Column(BigInteger, nullable=False, default=0)
    delete_time = Column(BigInteger, nullable=False, default=0)


class WxMpCfg(Base):
    __tablename__ = 'pay_wx_mp_cfg'
    id = Column(BigInteger, primary_key=True, index=True)
    cfg_name = Column(String, nullable=False, default='')
    mp_appid = Column(String, nullable=False, default='')
    mp_app_secret = Column(String, nullable=False, default='')
    auth_url_path = Column(String, nullable=False, default='')
    auth_content = Column(String, nullable=False, default='')
    encoding_aes_key = Column(String, nullable=False, default='')
    create_time = Column(BigInteger, nullable=False, default=0)
    update_time = Column(BigInteger, nullable=False, default=0)
    delete_time = Column(BigInteger, nullable=False, default=0)


class WxMiniappCfg(Base):
    __tablename__ = 'pay_wx_miniapp_cfg'
    id = Column(BigInteger, primary_key=True, index=True)
    cfg_name = Column(String, nullable=False, default='')
    mp_appid = Column(String, nullable=False, default='')
    mp_app_secret = Column(String, nullable=False, default='')
    create_time = Column(BigInteger, nullable=False, default=0)
    update_time = Column(BigInteger, nullable=False, default=0)
    delete_time = Column(BigInteger, nullable=False, default=0)


class WxOpenCfg(Base):
    __tablename__ = 'pay_wx_open_cfg'
    id = Column(BigInteger, primary_key=True, index=True)
    cfg_name = Column(String, nullable=False, default='')
    open_appid = Column(String, nullable=False, default='')
    create_time = Column(BigInteger, nullable=False, default=0)
    update_time = Column(BigInteger, nullable=False, default=0)
    delete_time = Column(BigInteger, nullable=False, default=0)


class Cfg(Base):
    __tablename__ = 'pay_cfg'
    id = Column(BigInteger, primary_key=True, index=True)
    pay_appid = Column(String, nullable=False, default='')
    pt = Column(String, nullable=False, default='')
    tp = Column(String, nullable=False, default='')
    cfg_id = Column(String, nullable=False, default='')
    create_time = Column(BigInteger, nullable=False, default=0)
    update_time = Column(BigInteger, nullable=False, default=0)
    delete_time = Column(BigInteger, nullable=False, default=0)


class UnifiedOrder(Base):
    __tablename__ = 'pay_unified_order'
    id = Column(BigInteger, primary_key=True, index=True)
    pay_appid = Column(String, nullable=False, default='')
    unified_order_id = Column(String, nullable=False, default='')
    pay_order_id = Column(String, nullable=False, default='')
    amount = Column(BigInteger, nullable=False, default=0)
    refund_amount = Column(BigInteger, nullable=False, default=0)
    extra = Column(String, nullable=False, default='')
    notify_url = Column(String, nullable=False, default='')
    return_url = Column(String, nullable=False, default='')
    pay_time = Column(BigInteger, nullable=False, default=0)
    expire_time = Column(BigInteger, nullable=False, default=0)
    last_refund_time = Column(BigInteger, nullable=False, default=0)
    create_time = Column(BigInteger, nullable=False, default=0)
    update_time = Column(BigInteger, nullable=False, default=0)


class PayOrder(Base):
    __tablename__ = 'pay_order'
    id = Column(BigInteger, primary_key=True, index=True)
    pay_appid = Column(String, nullable=False, default='')
    cfg_id = Column(BigInteger, nullable=False, default=0)
    pay_order_id = Column(String, nullable=False, default='')
    unified_order_id = Column(String, nullable=False, default='')
    pay_content = Column(String, nullable=False, default='')
    notify_content = Column(String, nullable=False, default='')
    last_notify_time = Column(BigInteger, nullable=False, default=0)
    create_time = Column(BigInteger, nullable=False, default=0)
    update_time = Column(BigInteger, nullable=False, default=0)


class AccessToken(Base):
    __tablename__ = 'pay_access_token'
    id = Column(BigInteger, primary_key=True, index=True)
    pt = Column(String, nullable=False, default='')
    appid = Column(String, nullable=False, default='')
    access_token = Column(String, nullable=False, default='')
    create_time = Column(BigInteger, nullable=False, default=0)
    expire_time = Column(BigInteger, nullable=False, default=0)
