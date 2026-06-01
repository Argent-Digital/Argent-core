import httpx
from typing import List

from src.schemas.vpn_schema import CreateKey, DelKeyData, VpnReturnData, DelKeysData, DeleteKeys, NodeData, CreateKeyClientBody
from src.schemas.jwt_schema import TokenData
from src.auth.security import create_access_token

class ArgentVpnClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(60.0, connect=5.0)
        )
    async def close(self):
        await self.client.aclose()

    async def create_key(self, user_data: CreateKey, node_data: NodeData) -> VpnReturnData:
        try:
            token_data = TokenData(user_id=user_data.user_id)
            token = create_access_token(data = token_data)

            url = "/vpn/create_key"
            header = {"Authorization": f"Bearer {token}" }
            body = CreateKeyClientBody(node_data=node_data, user_data = user_data)
            response = await self.client.post(url, json=body.model_dump(exclude_none=True), headers=header)
            response.raise_for_status()
            return VpnReturnData(**response.json())
        except Exception as e:
            print(f"Error send request of create key: {e}")
            return None
        
    async def sending_del_key(self, keys_list: List[DeleteKeys], nodes_list: List[NodeData], user_id: int = 0):
        try:
            token_data = TokenData(user_id=user_id)
            token = create_access_token(data = token_data)            
            url = "/vpn/cleaning_keys"
            header = {'Authorization': f"Bearer {token}"}
            body = DelKeysData(nodes_list=nodes_list, keys_list=keys_list)
            response = await self.client.post(url, json=body.model_dump(exclude_none=True), headers=header)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error send list keys to del: {e}")
            return None
        
    async def del_key(self, key_data: DeleteKeys, node_data: NodeData):
        try:
            token_data = TokenData(user_id=DeleteKeys.user_id)
            token = create_access_token(data=token_data)
            url = "/vpn/del_key"
            header = {'Authorization': f"Bearer {token}"}
            body = DelKeyData(node_data=node_data, key_data=key_data)
            response = await self.client.post(url, json=body.model_dump(exclude_none=True), headers=header)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error del key: {e}")
            return None