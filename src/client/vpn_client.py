import httpx
from src.schemas.vpn_schema import CreateKey, VpnReturnData

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
            url = f"{data.target_url.rstrip("/")}/vpn/create_key"
            header = {"X-API-KEY": data.api_key}
            response = await self.client.post(url, json=data.model_dump(), headers=header)
            response.raise_for_status()
            return VpnReturnData(**response.json())
        except Exception as e:
            print(f"Error send request of create key: {e}")
            return None