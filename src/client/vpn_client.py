import httpx
from typing import List

from src.schemas.vpn_schema import CreateKey, VpnReturnData, DeleteKeys, NodeData
from src.schemas.jwt_schema import TokenData
from src.auth.security import create_access_token

class ArgentVpnClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=httpx.Timeout(10.0, connect=5.0)
        )
    async def close(self):
        await self.client.aclose()

    async def create_key(self, data: CreateKey) -> VpnReturnData:
        try:
            token_data = TokenData(user_id=data.user_id)
            token = create_access_token(data = token_data)

            url = f"{data.target_url.rstrip('/')}/vpn/create_key"
            header = {"Authorization": f"Bearer {token}" }
            response = await self.client.post(url, json=data.model_dump(), headers=header)
            response.raise_for_status()
            return VpnReturnData(**response.json())
        except Exception as e:
            print(f"Error send request of create key: {e}")
            return None
        
    async def sending_del_key(self, data: List[DeleteKeys], node: NodeData, user_id: int = 0):
        try:
            token_data = TokenData(user_id=user_id)
            token = create_access_token(data = token_data)            
            payload = [k.model_dump() for k in data]
            url = f"{node.target_url.rstrip('/')}/vpn/clening_keys"
            header = {'Authorization': f"Bearer {token}"}
            body = {
                "api_key": node.api_key,
                "delete_keys": payload
            }
            response = await self.client.post(url, json=body, headers=header)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error send list keys to del: {e}")
            return None