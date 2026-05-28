from fastapi import APIRouter, Depends, HTTPException
from src.database.dao.vpn_dao import VpnKeyDao
from src.database.dao.node_dao import NodesDao
from src.schemas.vpn_schema import AccessUrlUser, DeleteKeys,DelKeyData, CreateKey, ReturnKeyForBot, NodeData
from src.client.vpn_client import ArgentVpnClient
from src.loader import get_vpn_client
from src.auth.dependencies import get_current_user_id

router = APIRouter(prefix="/vpn-core", tags=["Keys Vpn"])

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

@router.delete("/keys/del_key")
async def del_key(user_id: int = Depends(get_current_user_id), vpn_client: ArgentVpnClient = Depends(get_vpn_client)):
    key = await VpnKeyDao.get_user_vpn_data(user_id=user_id)
    if not key:
        raise HTTPException(status_code=404, detail="Don't search key")
    node_data = await NodesDao.node_by_id(node_id=key.nodes_id)

    del_data = DeleteKeys(
        user_id=user_id,
        server_key_id=key.server_key_id,
        protocol=key.protocol,
        vless_uuid=key.vless_uuid
    )
    if key.protocol == "vless":
        node = NodeData(
            ip=node_data.ip,
            ux_username=node_data.ux_username,
            ux_pass=node_data.ux_pass,
            ux_url=node_data.ux_url,
            vless_inbound=node_data.vless_inbound
        )
    else:
        node = NodeData(
            ip=node_data.ip,
            out_url=node_data.out_url,
            out_cert=node_data.out_cert
        )

    remote_data = await vpn_client.del_key(key_data=del_data, node_data=node)
    if not remote_data:
        raise HTTPException(status_code=505, detail="Don't push request")
    
    await VpnKeyDao.delete_vpn_key(user_id=user_id)

    return {"Status": "success"}

    
    

    