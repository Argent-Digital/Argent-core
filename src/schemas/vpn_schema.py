from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import List

class AccessUrlUser(BaseModel):
    access_url: str
    protocol: str

    model_config=ConfigDict(from_attributes=True)

class DeleteKeys(BaseModel):
    user_id: int
    nodes_id: int
    server_key_id: str| None = None
    protocol: str
    vless_uuid: UUID | None = None

    model_config=ConfigDict(from_attributes=True)

class NodeData(BaseModel):
    id: int
    ip: str

    ux_username: str | None = None
    ux_pass: str | None = None
    ux_url: str | None = None
    vless_inbound: int | None = None
    inbound_port: int | None = None
    path: str | None = None

    out_url: str | None = None
    out_cert: str | None = None

    model_config = ConfigDict(from_attributes=True)

class CreateKeyApiBody(BaseModel):
    protocol:str

class CreateKey(BaseModel):
    user_id: int
    protocol: str

    model_config = ConfigDict(from_attributes=True)

class CreateKeyClientBody(BaseModel):
    node_data: NodeData
    user_data: CreateKey

class VpnReturnData(BaseModel):
    server_key_id: str | None = None
    key_name: str
    access_url: str
    vless_uuid: UUID | None = None

class DelKeysData(BaseModel):
    nodes_list: List[NodeData]
    keys_list: List[DeleteKeys]

class DelKeyData(BaseModel):
    node_data: NodeData
    key_data: DeleteKeys