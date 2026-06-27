from fastapi import APIRouter, Depends, HTTPException
from src.database.dao.user_dao import UserDao
from src.database.dao.admin_dao import AdminDao
from src.schemas.bot_schema import UserRegister, CheckUserBalance, AdmUpdateBalance, UpdateBalance, StatsResponse
from src.auth.dependencies import get_current_user_id

router = APIRouter(prefix="/users", tags=['Users'])

@router.get("/check")
async def check_user(user_id: int = Depends(get_current_user_id)) -> bool:
    exists = await UserDao.check_user(user_id)
    return exists

@router.post("/register")
async def add_user(user_data: UserRegister):
    await UserDao.add_user(
        user_id=user_data.user_id,
        username=user_data.username,
        first_name=user_data.first_name,
        referrer_id=user_data.referrer_id
    )
    return {"status": "ok"}

@router.post("/adm_update_balance")
async def update_balance(user_data: AdmUpdateBalance, user_id: int = Depends(get_current_user_id)):
    await UserDao.update_balance(
        user_id=user_data.user_id,
        amount=user_data.amount
    )
    return {"status": "ok"}

@router.post("/update_balance")
async def update_balance(user_data: UpdateBalance, user_id: int = Depends(get_current_user_id)):
    await UserDao.update_balance(
        user_id=user_id,
        amount=user_data.amount
    )
    return {"status": "ok"}

@router.get("/get_balance", response_model=CheckUserBalance)
async def get_user_balance(user_id: int = Depends(get_current_user_id)):
    data = await UserDao.get_user_balance(user_id=user_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return CheckUserBalance(balance=data)

@router.get("/adm_stats", response_model=StatsResponse)
async def get_stats(user_id: int = Depends(get_current_user_id)):
    data = await AdminDao.get_stats()
    if data is None:
        raise HTTPException(status_code=404, detail="Don't search data")
    return data

@router.get("/get_users_list")
async def get_ids(user_id: int = Depends(get_current_user_id)):
    data = await UserDao.get_all_user_ids()
    return data