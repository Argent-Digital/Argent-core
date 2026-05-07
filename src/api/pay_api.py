from fastapi import APIRouter, Depends, HTTPException
from src.database.dao.user_dao import UserDao
from src.database.dao.vpn_dao import VpnKeyDao

router = APIRouter(prefix="/pay", tags=['pay'])

@router.post("/start_billig")
async def start_billing():
    await UserDao.daily_billing()
    data = await VpnKeyDao.billing_clining_keys()

    return {
        "deleted_count": len(data),
        "deleted_keys": data
    }
