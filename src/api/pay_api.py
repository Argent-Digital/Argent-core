from fastapi import APIRouter, Depends, HTTPException, status
from collections import defaultdict
from src.database.dao.user_dao import UserDao
from src.database.dao.vpn_dao import VpnKeyDao
from src.database.dao.node_dao import NodesDao
from src.schemas.vpn_schema import BillingResponse
from src.schemas.pay_chema import BillingStart
from src.client.vpn_client import ArgentVpnClient
from src.auth.dependencies import get_current_user_id

router = APIRouter(prefix="/pay", tags=['pay'])

async def veify_system_token(user_id: int = Depends(get_current_user_id)):
    if user_id != 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ только для системных сервисов"
        )
    return user_id

@router.post("/start_billing", response_model=BillingResponse)
async def start_billing(payload: BillingStart, system_id: int = Depends(veify_system_token)):
    if not payload.start:
        return {"deleted_count": 0, "deleted_keys": []}

    await UserDao.daily_billing()

    data = await VpnKeyDao.billing_clining_keys()
    grouped_by_node = defaultdict(list)
    for key in data:
        grouped_by_node[key["nodes_id"]].append(key)

    for node_id, keys in grouped_by_node.items():
        node_data = await NodesDao.node_by_id(node_id=node_id)
        await ArgentVpnClient.sending_del_key(data=keys, node=node_data)

    user_warning = await UserDao.users_with_low_balance()
    if data:
        user_ids_del = [k["user_id"] for k in data ]
        await VpnKeyDao.delete_keys(user_ids=user_ids_del)
    return {
        "deleted_count": len(data),
        "deleted_keys": data,
        "user_lower": user_warning
    }
