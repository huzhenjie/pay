from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.vo import res_success
from app.vo import schemas
from app.dao.database import get_db
from app.service import order

router = APIRouter()


@router.post("/pay/unified-order")
async def create_user(vo: schemas.UnifiedOrderVo, db: Session = Depends(get_db)):
    order_info = order.Order.create_unified_order(vo, db)
    return res_success(order_info)


@router.get("/pay/unified-order/{unified_order_id}")
async def get_unified_order_detail(unified_order_id, db: Session = Depends(get_db)):
    order_info = order.Order.get_unified_order_detail(unified_order_id, db)
    return res_success(order_info)
