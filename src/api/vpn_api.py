from fastapi import APIRouter, Depends, HTTPException
from src.database.dao.vpn_dao import VpnKeyDao
from src.schemas.vpn_schema import AccessUrlUser, CreateKey, ReturnKeyForBot
from src.client.vpn_client import ArgentVpnClient

router = APIRouter(prefix="/vpn", tags=["Keys Vpn"])

@router.get("/keys/access_url/{user_id}", response_model=AccessUrlUser)
async def get_user_access_url(user_id: int):
    key_data = await VpnKeyDao.get_user_access_url(user_id=user_id)
    if not key_data:
        raise HTTPException(status_code=404, detail="ключ не найден")
    return key_data

@router.post("/create_key/{user_id}", response_model=ReturnKeyForBot)
async def create_new_vpn_key(user_id: int, protocol: str): 
    node = await VpnKeyDao.optimized_select_nodes()

    if node is None:
        return {"error": "No active nodes available"}
    
    create_key_data = CreateKey(
        user_id=user_id,
        protocol=protocol,
        target_url=f"https://{node.ip}:8002",
        api_key=node.api_key
    )

    vpn_client = ArgentVpnClient(base_url=create_key_data.target_url)

    remote_data = await vpn_client.create_key(data=create_key_data)

    if not remote_data:
        raise HTTPException(status_code=500, detail="Server not answer or error")
    
    await VpnKeyDao.add_vpn_key(
        user_id=user_id,
        key_name=remote_data.key_name,
        access_url=remote_data.access_url,
        node_id=node.id,
        protocol=protocol,
        server_key_id=remote_data.server_key_id,
        vless_uuid=remote_data.vless_uuid
    )

    return ReturnKeyForBot(access_url=remote_data.access_url, protocol=protocol)