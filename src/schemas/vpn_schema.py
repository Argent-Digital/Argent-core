from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List, Optional
from src.schemas.pay_chema import UserWithLowBalance

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

    model_config=ConfigDict(from_attributes=True)

class BillingResponse(BaseModel):
    status: str = "success"
    deleted_keys: List[DeleteKeys]
    user_lower: List[UserWithLowBalance]

class NodeData(BaseModel):
    ip: str

    ux_username: str | None
    ux_pass: str | None
    ux_url: str | None

    out_url: str | None
    out_cert: str | None

    model_config = ConfigDict(from_attributes=True)

class CreateKey(BaseModel):
    user_id: int
    protocol: str

    model_config = ConfigDict(from_attributes=True)

class CreateKeyClientBody(BaseModel):
    node_data: NodeData
    user_data: CreateKey

class VpnReturnData(BaseModel):
    server_key_id: str | None
    key_name: str
    access_url: str
    vless_uuid: UUID | None

class ReturnKeyForBot(BaseModel):
    access_url: str
    protocol: str

class DelKeysData(BaseModel):
    nodes_list: List[NodeData]
    keys_list: List[DeleteKeys]