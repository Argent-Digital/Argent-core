
from pydantic import BaseModel, ConfigDict


class BillingStart(BaseModel):
    start: bool

class UserWithLowBalance(BaseModel):
    user_id: int

    model_config=ConfigDict(from_attributes=True)

class BillingResponse(BaseModel):
    deleted_keys: list[int]
    user_lower: list[int]

class UserUpdateBalance(BaseModel):
    amount:int
