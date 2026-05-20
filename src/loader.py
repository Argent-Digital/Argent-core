from src.config import settings
from src.client.vpn_client import ArgentVpnClient

_vpn_client = ArgentVpnClient(base_url=settings.VPN_SERVICE_URL)

async def get_vpn_client() -> ArgentVpnClient:
    return _vpn_client