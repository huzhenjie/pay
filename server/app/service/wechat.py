import json
import time
import requests
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, or_
from app.dao.database import get_db
from app.dao import models


class Wechat():

    @staticmethod
    def save_mp_notify(db, appid, openid, ts, msg_type, content):
        now_ts = int(time.time())
        info = models.WxMpNotify(
            mp_appid=appid,
            openid=openid if openid else '',
            ts=ts if ts else now_ts,
            msg_type=msg_type,
            content=content,
            create_time=now_ts
        )
        db.add(info)
        db.commit()

    @staticmethod
    def get_access_token(db, pt, appid):
        now_ts = int(time.time())
        access_token = db.query(models.AccessToken) \
            .filter(models.AccessToken.appid == appid) \
            .order_by(models.AccessToken.id.desc()) \
            .first()
        if access_token and access_token.expire_time > now_ts + 60 and access_token.access_token:
            return {
                'access_token': access_token.access_token,
                'expires_in': access_token.expire_time - now_ts
            }
        secret = None
        if pt == 'wx_mp_cfg':
            cfg = db.query(models.WxMpCfg) \
                .filter(and_(models.WxMpCfg.mp_appid == appid, models.WxMpCfg.delete_time == 0)) \
                .first()
            if not cfg:
                raise HTTPException(status_code=404, detail='没有找到appid=%s的相关配置信息' % appid)
            secret = cfg.mp_app_secret
        if not secret:
            raise HTTPException(status_code=404, detail='没有找到pt=%s的相关配置信息' % pt)
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            appid, secret)
        # {
        #   "errcode": 40013,
        #   "errmsg": "invalid appid, rid: 6482ef52-53df6042-1f53f707"
        # }
        # {
        #   "access_token": "69_jTmo2RGzEseO3ofBPKqXn5Xjd1KlLCHKHsjXz89nGPoPlUucR-uGbJIwp9h48gTVGjMmEb-Qn-M5TccacSs73751fXIzk34PczVJK-YOpdbqX7h_Bc4fX2iO-cYSEIjADAVHL",
        #   "expires_in": 7200
        # }
        res = requests.post(url)
        res_text = res.text
        res_obj = json.loads(res.text)
        access_token_str = res_obj.get('access_token')
        if not access_token_str:
            raise HTTPException(status_code=500, detail='获取AccessToken失败 %s' % res_text)
        expires_in = res_obj.get('expires_in')
        db_access_token = models.AccessToken(
            pt=pt,
            appid=appid,
            access_token=access_token_str,
            expire_time=now_ts + expires_in,
            create_time=now_ts
        )
        db.add(db_access_token)
        db.commit()
        return {
            'access_token': access_token_str,
            'expires_in': expires_in
        }

    @staticmethod
    def get_mp_auth_content(db, path):
        cfg = db.query(models.WxMpCfg) \
            .filter(and_(models.WxMpCfg.auth_url_path == path, models.WxMpCfg.delete_time == 0)) \
            .first()
        if not cfg:
            return 'Unknown path: %s' % path
        return cfg.auth_content

    @staticmethod
    def get_open_id():
        appid = ''
        secret = ''
        code = ''
        api = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'
        res = requests.post(api)
        print(res.text)
        # res = requests.post('https://yinqiantong.com/test', data=post_data) post from
        # res = requests.post('https://yinqiantong.com/test', json=post_data) post json
        # print(res.text)
