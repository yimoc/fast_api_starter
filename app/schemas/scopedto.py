from pydantic import BaseModel

class ScopeCreate(BaseModel):
    permission: str
    description: str

class ScopeUpdate(ScopeCreate):
    pass

class ScopeResponse(BaseModel):
    id: int
    permission: str
    description: str
    class Config:
        from_attributes = True

