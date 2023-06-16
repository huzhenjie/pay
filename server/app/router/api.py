from fastapi import APIRouter, Depends, Request
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

