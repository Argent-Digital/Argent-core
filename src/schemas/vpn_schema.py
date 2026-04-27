from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class AccessUrlUser(BaseModel):
    key_id: int
    user_id: int
    server_key_id: str
    key_name: str
    access_url: str
    created_at: datetime
    protocol: str
    vless_uuid: UUID

    model_config=ConfigDict(from_attributes=True)