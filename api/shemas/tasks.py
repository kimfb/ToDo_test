from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title:  Annotated[str, MinLen(3), MaxLen(40)]
    description: Annotated[str, MinLen(5)]


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TaskCreate(TaskBase):
    user_name: str
    user_surname: str


class TasksByUser(TaskBase):
    user_name: str
    user_surname: str
    created_at: datetime
    updated_at: Optional[datetime]


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
