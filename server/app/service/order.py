from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, or_
import time

from app.vo import schemas
from app.dao.database import get_db
from app.dao import models


class Order():
    @staticmethod
    def create_unified_order(vo: schemas.UnifiedOrderVo, db: Session = Depends(get_db)):
        app = db.query(models.App) \
            .filter(and_(models.App.pay_appid == vo.pay_appid, models.App.delete_time == 0)) \
            .first()
        if not app:
            raise HTTPException(status_code=404, detail='没有找到相关App信息')
        if app.allow_payment != 'Y':
            raise HTTPException(status_code=403, detail='当前App支付通道已关闭')
        now_ts = int(time.time())
        expire_time = now_ts + 7200
        if vo.expire_time > 0:
            if vo.expire_time < now_ts + 60:
                raise HTTPException(status_code=400, detail='过期时间须大于当前时间1分钟')
            expire_time = vo.expire_time
        order = models.UnifiedOrder(
            pay_appid=vo.pay_appid,
            unified_order_id=vo.unified_order_id,
            amount=vo.amount,
            expire_time=expire_time,
            extra=vo.extra,
            notify_url=vo.notify_url,
            return_url=vo.return_url
        )
        try:
            db.add(order)
            db.flush()
            db.commit()
            return order.id
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail='创建订单失败')

    @staticmethod
    def get_unified_order_detail(unified_order_id, db: Session = Depends(get_db)):
        unified_order = db.query(models.UnifiedOrder) \
            .filter(models.UnifiedOrder.unified_order_id == unified_order_id) \
            .first()
        if not unified_order:
            raise HTTPException(status_code=404, detail='没有找到相关订单信息')
        app = db.query(models.App) \
            .filter(and_(models.App.pay_appid == unified_order.pay_appid, models.App.delete_time == 0)) \
            .first()
        if not app:
            raise HTTPException(status_code=404, detail='没有找到相关App信息')
        cfg_list = db.query(models.Cfg) \
            .filter(and_(models.Cfg.pay_appid == unified_order.pay_appid, models.Cfg.delete_time == 0)) \
            .order_by(models.Cfg.pt.asc(), models.Cfg.tp.asc()) \
            .all()
        if len(cfg_list) == 0:
            raise HTTPException(status_code=400, detail='暂无支付配置')
        res_cfg = []
        for cfg in cfg_list:
            res_cfg_item = {
                'pt': cfg.pt,
                'tp': cfg.tp,
                'cfg_id': cfg.cfg_id,
            }
            if cfg.pt == 'wx_mp_cfg':
                curr_cfg = db.query(models.WxMpCfg) \
                    .filter(and_(models.WxMpCfg.id == cfg.cfg_id, models.WxMpCfg.delete_time == 0)) \
                    .first()
                if not curr_cfg:
                    continue
                res_cfg_item['appid'] = curr_cfg.mp_appid
            elif cfg.pt == 'wx_miniapp_cfg':
                curr_cfg = db.query(models.WxMiniappCfg) \
                    .filter(and_(models.WxMiniappCfg.id == cfg.cfg_id, models.WxMiniappCfg.delete_time == 0)) \
                    .first()
                if not curr_cfg:
                    continue
                res_cfg_item['appid'] = curr_cfg.mp_appid
            elif cfg.pt == 'wx_open_cfg':
                curr_cfg = db.query(models.WxOpenCfg) \
                    .filter(and_(models.WxOpenCfg.id == cfg.cfg_id, models.WxOpenCfg.delete_time == 0)) \
                    .first()
                if not curr_cfg:
                    continue
                res_cfg_item['appid'] = curr_cfg.open_appid
            else:
                continue
            res_cfg.append(res_cfg_item)
        now_ts = int(time.time())
        return {
            'app': {
                'appname': app.appname,
                'pay_appid': app.pay_appid,
            },
            'pay_cfg': res_cfg,
            'order': {
                'unified_order_id': unified_order_id,
                'amount': unified_order.amount,
                'refund_amount': unified_order.refund_amount,
                'last_refund_time': unified_order.last_refund_time,
                'create_time': unified_order.create_time,
                'pay_time': unified_order.pay_time,
                'expire_in': unified_order.expire_time - now_ts,
                'return_url': unified_order.return_url,
            }
        }

    @staticmethod
    def get_unified_order_state(unified_order_id, db: Session = Depends(get_db)):
        unified_order = db.query(models.UnifiedOrder) \
            .filter(models.UnifiedOrder.unified_order_id == unified_order_id) \
            .first()
        if not unified_order:
            raise HTTPException(status_code=404, detail='没有找到相关订单信息')
        return {
            'pay_time': unified_order.pay_time
        }

