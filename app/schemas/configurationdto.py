from datetime import datetime
from typing import Union, List
from uuid import UUID

from pydantic import BaseModel


class ConfigurationCreate(BaseModel):
    key: str
    value: str
    description: Union[str, None] = None

    # class Config:
    #     orm_mode = True


class ConfigurationUpdate(BaseModel):
    value: str
    description: Union[str, None] = None

    # class Config:
    #     orm_mode = True


class ConfigurationResponse(BaseModel):
    id: UUID
    key: str
    value: str
    description: Union[str, None] = None

    class Config:
        from_attributes = True