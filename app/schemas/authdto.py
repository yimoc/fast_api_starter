from typing import Union, List

from pydantic import BaseModel

from app.schemas.userdto import UserResponse

class UserLogin(BaseModel):
    email: Union[str, None] = None
    password: Union[str, None] = None
    hash: Union[str, None] = None       # "id+' '+ password"를 해시함
    #docs용 test code
    username: Union[str, None] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class Key(BaseModel):
    key: str

class TokenData(BaseModel):
    username: Union[str, None] = None
    email : str
    scopes: List[str] = []
