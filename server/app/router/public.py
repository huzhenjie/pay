from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
import time
import json
import xmltodict

from app.service import wechat
from app.dao import models
from app.vo import res_success
from app.vo import schemas

router = APIRouter()


@router.get("/test")
@router.post("/test")
async def create_user(request: Request):
    # db = request.app.state.db()
    body_str = await request.body()
    return res_success({
        'req_header': request.headers,
        'req_body': body_str,
        'server_ts': time.time()
    })


@router.get("/MP_verify_{verify_id}.txt", response_class=PlainTextResponse)
def create_user(request: Request, verify_id):
    full_path = "MP_verify_%s.txt" % verify_id
    db = request.app.state.db()
    return wechat.Wechat.get_mp_auth_content(db, full_path)


@router.get("/wx/mp/notify/{appid}")
async def deal_mp_notify(appid: str,
                         signature: str = None,
                         echostr: str = None,
                         timestamp: str = None,
                         nonce: str = None):
    return PlainTextResponse(echostr)


@router.post("/wx/mp/notify/{appid}")
async def deal_mp_notify(request: Request,
                         appid: str,
                         signature: str = None,
                         timestamp: str = None,
                         nonce: str = None,
                         openid: str = None,
                         encrypt_type: str = None,  # aes
                         msg_signature: str = None):
    db = request.app.state.db()
    req_sign_ok = wechat.Wechat.verify_mp_sign(db, appid, signature, timestamp, nonce)
    if not req_sign_ok:
        print('Req sign error')
        return PlainTextResponse('')
    req_content_type = request.headers['Content-Type']
    body_str = await request.body()
    print("[MpNotify][Appid:%s][Openid:%s][ContentType:%s]: %s" % (appid, openid, req_content_type, body_str))
    if req_content_type == 'text/xml':
        body = xmltodict.parse(body_str)
        print(body)
        xml = body.get('xml')
        encrypt = xml.get('Encrypt')
        msg_sign_ok = wechat.Wechat.verify_mp_msg_sign(db, appid, msg_signature, timestamp, nonce, encrypt)
        if not msg_sign_ok:
            print('Msg sign error')
            return PlainTextResponse('')
        xml_content = wechat.Wechat.decrypt_msg_content(db, appid, encrypt)
        if not xml_content:
            print('Decrypt msg error')
            return PlainTextResponse('')
        msg_xml = xmltodict.parse(xml_content)
        msg_content = msg_xml.get('xml')
        ts = msg_content.get('CreateTime', timestamp)
        msg_type = msg_content.get('MsgType')
        msg_content_str = json.dumps(msg_content)
        wechat.Wechat.save_mp_notify(db, appid, openid, ts, msg_type, body_str, msg_content_str)
    return PlainTextResponse('')

