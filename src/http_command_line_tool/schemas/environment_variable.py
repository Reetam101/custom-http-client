from pydantic import BaseModel, ConfigDict
from typing import Optional

class EnvironmentVariableCreate(BaseModel):
    key: str
    value: str
    is_secret: Optional[bool] = False

class EnvironmentVariableResponse(BaseModel):
    id: int
    key: str
    is_secret: bool

    model_config = ConfigDict(from_attributes=True)


    