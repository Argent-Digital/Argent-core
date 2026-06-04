from fastapi import APIRouter, Depends, HTTPException, status
import logging
from src.database.dao.user_dao import UserDao
from src.database.dao.vpn_dao import VpnKeyDao
from src.database.dao.node_dao import NodesDao
from src.schemas.pay_chema import BillingStart, BillingResponse
from src.client.vpn_client import ArgentVpnClient
from src.loader import get_vpn_client
from src.auth.verify_system_token import veify_system_token

router = APIRouter(prefix="/pay", tags=['pay'])
logger = logging.getLogger(__name__)

@router.post("/start_billing", response_model=BillingResponse)
async def start_billing(payload: BillingStart, vpn_client: ArgentVpnClient = Depends(get_vpn_client), system_id: int = Depends(veify_system_token)):
    if not payload:
        raise HTTPException(status_code=404, detail="Not conf billing")

    await UserDao.daily_billing()

    data = await VpnKeyDao.billing_clining_keys()
    user_warning = await UserDao.users_with_low_balance()
    if data:
        node_list = await NodesDao.select_nodes_list()
        
        try:
            dels_key = await vpn_client.sending_del_key(keys_list=data, nodes_list=node_list)
            if not dels_key:
                logger.warning("VPN-микросервис вернул False при удалении ключей, но мы продолжаем!")
        except Exception as e:
            logger.error(f"Не удалось достучаться до VPN-сервиса: {e}. Ключи будут удалены локально.")

    if data:
        user_ids_del = [k["user_id"] for k in data ]
        await VpnKeyDao.delete_keys(user_ids=user_ids_del)
    return BillingResponse(deleted_keys=user_ids_del, user_lower=user_warning)
