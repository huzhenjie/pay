from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.vo import res_success
from app.vo import schemas
from app.dao.database import get_db
from app.service import wechat

router = APIRouter()


@router.post("/api/wx/mp/access-token")
async def get_access_token(vo: schemas.GetWxAccessTokenVo, db: Session = Depends(get_db)):
    access_token_info = wechat.Wechat.get_access_token(vo.pt, vo.appid, db)
    return res_success(access_token_info)


@router.post("/api/wx/mp/notify/{app_id}")
async def deal_mp_notify(request: Request,
                         app_id: str,
                         echostr: str = None,
                         signature: str = None,
                         timestamp: str = None,
                         nonce: str = None,
                         openid: str = None):
    req_content_type = request.headers['Content-Type']
    body = await request.body()
    print("[MpNotify][appid:%s][openid:%s][%s]: %s" % (app_id, openid, req_content_type, body))
    if echostr:
        return PlainTextResponse(echostr)
    if req_content_type == 'application/xml':
        pass
    return res_success(body)
