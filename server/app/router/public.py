from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import time
import xmltodict

from app.dao import models
from app.vo import res_success
from app.vo import schemas
from app.dao.database import get_db
from app.service import wechat

router = APIRouter()


# curl -X POST -H 'Content-Type: application/json' -d '{"keyword": "小"}' http://192.168.96.11:8788/test
@router.get("/test")
@router.post("/test")
async def create_user(request: Request, db: Session = Depends(get_db)):
    body_str = await request.body()
    return res_success({
        'req_header': request.headers,
        'req_body': body_str,
        'server_ts': time.time()
    })


@router.get("/MP_{path}.txt", response_class=PlainTextResponse)
def create_user(path, db: Session = Depends(get_db)):
    full_path = "MP_%s.txt" % path
    return wechat.Wechat.get_mp_auth_content(full_path, db)


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
    req_content_type = request.headers['Content-Type']
    body_str = await request.body()
    print("[MpNotify][Appid:%s][Openid:%s][ContentType:%s]: %s" % (appid, openid, req_content_type, body_str))
    if req_content_type == 'text/xml':
        body = xmltodict.parse(body_str)
        print(body)
        xml = body.get('xml')
        ts = xml.get('CreateTime', timestamp)
        msg_type = xml.get('MsgType')
        wechat.Wechat.save_mp_notify(appid, openid, ts, msg_type, body_str)
    return PlainTextResponse('')
