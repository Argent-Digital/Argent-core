from pydantic import ConfigDict, BaseModel
from typing import Optional

class TokenData(BaseModel):
    user_id: Optional[int] = None