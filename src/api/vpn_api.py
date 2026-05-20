from fastapi import APIRouter, Depends, HTTPException
from src.database.dao.vpn_dao import VpnKeyDao
from src.schemas.vpn_schema import AccessUrlUser, CreateKey, ReturnKeyForBot, NodeData
from src.client.vpn_client import ArgentVpnClient
from src.loader import get_vpn_client
from src.config import settings
from src.auth.dependencies import get_current_user_id

router = APIRouter(prefix="/vpn", tags=["Keys Vpn"])

@router.get("/keys/access_url", response_model=AccessUrlUser)
async def get_user_access_url(user_id: int = Depends(get_current_user_id)):
    key_data = await VpnKeyDao.get_user_access_url(user_id=user_id)
    if not key_data:
        raise HTTPException(status_code=404, detail="ключ не найден")
    return key_data

@router.post("/create_key", response_model=ReturnKeyForBot)
async def create_new_vpn_key(protocol: str, user_id: int = Depends(get_current_user_id), vpn_client: ArgentVpnClient = Depends(get_vpn_client)): 
    node = await VpnKeyDao.optimized_select_nodes()

    if node is None:
        raise HTTPException(status_code=404, detail="No active node")
    
    create_key_data = CreateKey(
        user_id=user_id,
        protocol=protocol,
    )

    if protocol == "vless":
        node_data = NodeData(
            ip=node.ip,
            ux_username=node.ux_username,
            ux_pass=node.ux_pass,
            ux_url=node.ux_url
        )
    else:
        node_data = NodeData(
            ip=node.ip,
            out_url=node.out_url,
            out_cert=node.out_cert
        )

    remote_data = await vpn_client.create_key(user_data=create_key_data, node_data=node_data)

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