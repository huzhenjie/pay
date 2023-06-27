import json
import time
import base64
import socket
import struct
import hashlib
import requests
from Crypto.Cipher import AES
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_, or_
from app.dao.database import get_db
from app.dao import models


class Wechat():

    @staticmethod
    def save_mp_notify(db, appid, openid, ts, msg_type, origin_content, msg_content_str):
        now_ts = int(time.time())
        info = models.WxMpNotify(
            mp_appid=appid,
            openid=openid if openid else '',
            ts=ts if ts else now_ts,
            msg_type=msg_type,
            content=msg_content_str,
            origin_content=origin_content,
            create_time=now_ts
        )
        db.add(info)
        db.commit()

    @staticmethod
    def get_access_token(db, pt, appid, ignore_cache=False):
        now_ts = int(time.time())
        if not ignore_cache:
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
        # {
        #   "errcode": 40013,
        #   "errmsg": "invalid appid, rid: 6482ef52-53df6042-1f53f707"
        # }
        # {
        #   "access_token": "69_jTmo2RGzEs1O3ofBPKqXn5Xjd1KlLCHKHsjXz89nGPoPlUucR-uGbJIwp9h48gTVGjMmEb-Qn-M5TccacSs73751fXIzk34PczVJK-YOpdbqX7h_Bc4fX2iO-cYSEIjADAVHL",
        #   "expires_in": 7200
        # }
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            appid, secret)
        res = requests.post(url)
        # url = 'https://api.weixin.qq.com/cgi-bin/stable_token'
        # res = requests.post(url, json={
        #     'grant_type': 'client_credential',
        #     'appid': appid,
        #     'secret': secret
        # })
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
    def verify_mp_sign(db, appid, req_signature, timestamp, nonce):
        cfg = db.query(models.WxMpCfg) \
            .filter(and_(models.WxMpCfg.mp_appid == appid, models.WxMpCfg.delete_time == 0)) \
            .first()
        if not cfg:
            return False
        data = [cfg.token, timestamp, nonce]
        data.sort()
        origin_str = "".join(data)
        server_signature = hashlib.sha1(origin_str.encode("utf-8")).hexdigest()
        return server_signature == req_signature

    @staticmethod
    def verify_mp_msg_sign(db, appid, req_msg_signature, timestamp, nonce, encrypt):
        cfg = db.query(models.WxMpCfg) \
            .filter(and_(models.WxMpCfg.mp_appid == appid, models.WxMpCfg.delete_time == 0)) \
            .first()
        if not cfg:
            return False
        data = [cfg.token, timestamp, nonce, encrypt]
        data.sort()
        origin_str = "".join(data)
        server_signature = hashlib.sha1(origin_str.encode("utf-8")).hexdigest()
        return server_signature == req_msg_signature

    @staticmethod
    def decrypt_msg_content(db, appid, encrypt):
        cfg = db.query(models.WxMpCfg) \
            .filter(and_(models.WxMpCfg.mp_appid == appid, models.WxMpCfg.delete_time == 0)) \
            .first()
        if not cfg:
            print('WxMpCfg not found appid=%s' % appid)
            return None
        aes_key = base64.b64decode(cfg.encoding_aes_key + "=")
        encrypted_msg = base64.b64decode(encrypt)
        iv = encrypted_msg[:16]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_text = cipher.decrypt(encrypted_msg)
        pad = decrypted_text[-1]
        decrypted_text = decrypted_text[16:-pad]
        xml_len = socket.ntohl(struct.unpack("I", decrypted_text[: 4])[0])
        xml_content = decrypted_text[4: xml_len + 4]
        from_appid = decrypted_text[xml_len + 4:].decode('utf-8')
        if from_appid != appid:
            print('appid not equal，Encrypt_appid=%s Req_appid=%s' % (from_appid, appid))
            return None
        return xml_content

    @staticmethod
    def get_media_list(db, appid, media_type, offset, count=20):
        """
        :param media_type: image / video / voice / news
        :param offset: should >= 0
        :param count: should <= 20
        :return:
        """
        access_token = Wechat.get_access_token(db, 'wx_mp_cfg', appid)
        api = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s'\
              % access_token.get('access_token')
        res = requests.post(api, json={
            'type': media_type,
            'offset': offset,
            'count': count
        })
        # {"item":[{"media_id":"GWnKnmoJBxxxs7j3gvTfp11Neuk2HiM4mC3fq2xYMG0xvUSwyiKeoPhDFgCFef2j","name":"xxx.png","update_time":1680491706,"url":"https:\/\/mmbiz.qpic.cn\/mmbiz_png\/YZYh6zDpiarBFchfwrzYMpiclkTnVgYlC2lfPJHc9cIS9Mq3KKLPic4v45LoHkK8LDM6pZaJwsqx000AXT3OetYic4g\/0?wx_fmt=png","tags":[]}],"total_count":10,"item_count":10}
        res_obj = json.loads(res.text)
        return res_obj

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
