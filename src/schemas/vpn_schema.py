from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List, Optional

class AccessUrlUser(BaseModel):
    key_id: int
    user_id: int
    server_key_id: str | None
    key_name: str
    access_url: str
    created_at: datetime
    protocol: str
    vless_uuid: UUID | None

    model_config=ConfigDict(from_attributes=True)

class DeleteKeys(BaseModel):
    user_id: int
    server_key_if: Optional[str]
    protocol: str
    vless_uuid: Optional[UUID]

class BillingResponse(BaseModel):
    status: str = "success"
    deleted_count: int
    deleted_keys: List[DeleteKeys]