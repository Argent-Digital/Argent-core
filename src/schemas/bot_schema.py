from pydantic import BaseModel, ConfigDict

class UserRegister(BaseModel):
    user_id:int
    username:str | None = None
    first_name:str
    referer_id:int | None = None


class UserUpdateBalance(BaseModel):
    user_id:int
    amount:int

class CheckUserBalance(BaseModel):
    balance: int

    model_config = ConfigDict(from_attributes=True)

