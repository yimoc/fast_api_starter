from datetime import datetime
from typing import Union, List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.scopedto import ScopeResponse, ScopeUpdate
from app.schemas.userdto import UserResponse


class UploadFileCreate(BaseModel):
    name: str
    size: int
    path: str

class UploadFileResponse(BaseModel):
    id: UUID
    name: str
    size: int
    path: str
    created_at: datetime

    class Config:
        from_attributes = True


