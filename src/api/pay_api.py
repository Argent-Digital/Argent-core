from fastapi import APIRouter, Depends, HTTPException
from src.database.dao.user_dao import UserDao
from src.database.dao.vpn_dao import VpnKeyDao
from src.schemas.vpn_schema import BillingResponse
from src.schemas.pay_chema import BillingStart

router = APIRouter(prefix="/pay", tags=['pay'])

@router.post("/start_billig", response_model=BillingResponse)
async def start_billing(payload: BillingStart):
    if not payload.start:
        return {"deleted_count": 0, "deleted_keys": []}

    await UserDao.daily_billing()
    data = await VpnKeyDao.billing_clining_keys()

    return {
        "deleted_count": len(data),
        "deleted_keys": data
    }
