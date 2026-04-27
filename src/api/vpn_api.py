from fastapi import APIRouter, Depends, HTTPException
from src.database.dao.vpn_dao import VpnKeyDao
from src.schemas.vpn_schema import AccessUrlUser

router = APIRouter(prefix="/vpn", tags=["Keys Vpn"])

@router.get("/keys/access_url/{user_id}", response_model=AccessUrlUser)
async def get_user_access_url(user_id: int):
    key_data = await VpnKeyDao.get_user_access_url(user_id=user_id)
    if not key_data:
        raise HTTPException(status_code=404, detail="ключ не найден")
    return key_data