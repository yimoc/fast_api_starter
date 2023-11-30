from datetime import datetime
from typing import Union, List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.scopedto import ScopeResponse, ScopeUpdate


class UserCreate(BaseModel):
    #userid: Union[str, None] = None
    name: Union[str, None] = None
    email: str
    password: str
    scopes: List[ScopeUpdate]
    is_active: bool

class UserUpdate(BaseModel):
    #userid: Union[str, None] = None
    name: Union[str, None] = None
    #email: Union[str, None] = None
    password: Union[str, None] = None
    scopes: Union[List[ScopeUpdate], None] = None
    is_active: Union[bool, None] = None

class UserInitPassword(BaseModel):
    password: Union[str, None] = None
    hash: Union[str, None] = None  # password hash

class UserResponse(BaseModel):
    id: UUID
    #userid: str
    name: Union[str, None] = None
    email: str
    scopes: List[ScopeResponse]
    is_active: bool
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    class Config:
        from_attributes = True



