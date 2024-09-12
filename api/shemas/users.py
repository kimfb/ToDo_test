from typing import Annotated
from annotated_types import MinLen, MaxLen

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    user_name: Annotated[str, MinLen(2), MaxLen(20)]
    user_surname: Annotated[str, MinLen(2), MaxLen(20)]


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
