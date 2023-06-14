from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.dao import models
from app.vo import res_success
from app.vo import schemas
from app.dao.database import get_db
from app.service import wechat

router = APIRouter()


# curl -X POST -H 'Content-Type: application/json' -d '{"keyword": "小"}' http://192.168.96.11:8788/test
@router.post("/test")
def create_user(user: schemas.StuSearchVo, db: Session = Depends(get_db)):
    return res_success()


@router.get("/{path}", response_class=PlainTextResponse)
def create_user(path, db: Session = Depends(get_db)):
    return wechat.Wechat.get_mp_auth_content(path, db)
