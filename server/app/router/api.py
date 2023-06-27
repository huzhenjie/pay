from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.vo import res_success
from app.vo import schemas
from app.dao.database import get_db
from app.service import wechat

router = APIRouter()


@router.post("/api/wx/mp/access-token")
async def get_access_token(vo: schemas.GetWxAccessTokenVo, db: Session = Depends(get_db)):
    access_token_info = wechat.Wechat.get_access_token(db, vo.pt, vo.appid, vo.ignore_cache)
    return res_success(access_token_info)


@router.get("/api/wx/mp/{appid}/media-list")
async def get_media_list(request: Request, appid, media_type, offset: int = 0, count: int = 20):
    db = request.app.state.db()
    data = wechat.Wechat.get_media_list(db, appid, media_type, offset, count)
    return res_success(data)
