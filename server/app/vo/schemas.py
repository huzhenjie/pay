from pydantic import BaseModel
from typing import Union, Optional


class StuSearchVo(BaseModel):
    keyword: Optional[str] = ''
    # classroom_id: int = 0


class UnifiedOrderVo(BaseModel):
    pay_appid: str
    unified_order_id: str
    amount: int
    expire_time: Optional[int] = 0
    extra: Optional[str] = ''
    notify_url: Optional[str] = ''
    return_url: Optional[str] = ''


class GetWxAccessTokenVo(BaseModel):
    appid: str
    pt: str
    ignore_cache: Optional[bool] = False
