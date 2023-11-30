import base64
import logging
from datetime import datetime, timedelta
from typing import Annotated, Union

# from Crypto.Cipher import PKCS1_v1_5
# from Crypto.PublicKey import RSA
# from Crypto.Random import get_random_bytes
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from fastapi import Depends, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)

from jose import JWTError, jwt, ExpiredSignatureError
from pydantic import ValidationError
from starlette.responses import Response

from app.common.exceptions import invalidLoginError, unauthorizedError, noPermissionError, expiredTokenError
from app.core.sqlalchemy.database import db_connector
from app.orm.user_orm import select_by_email
from app.schemas.authdto import Key, LoginResponse, UserLogin, TokenData
from app.services.password import verify_password

logger = logging.getLogger(__name__)

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "68d1062c6de59327e94e93d7b2790028ed1db458d5a7ae87706bde62c13369ef"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

COOKIE_PRIVATE_KEY_NAME="session-no"

oauth2_scheme = OAuth2PasswordBearer(
    #tokenUrl="/api/v1/auth/loginForm",  #test용
    tokenUrl="/api/v1/auth/login",    #실제사용
    scopes={
        "user": "user",
        "admin" : "administrator"
        #"template": "Read information about the current user.",
        #"anylsis": "Read items.",
    },
    auto_error=False
)

def get_model_dict(model):
    return dict((column.name, getattr(model, column.name))
                for column in model.__table__.columns)

async def login(request: Request, session, user: UserLogin):

    user_base = await select_by_email(session, email=user.email)
    if not user_base:
        logging.info(f'failed : email = {user.email}')
        raise invalidLoginError
    if not verify_password(user.password, user_base.hashed_password):
        logging.info(f'failed : password {user.password} != {user_base.hashed_password}')
        raise invalidLoginError
    if not user_base.is_active:
        logging.info(f'failed : active = {user_base.is_active}')
        raise invalidLoginError
    logging.debug("Done Checking : id, pw, active")

    #make token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    list_scopes = [ db_base.permission for db_base in user_base.scopes]
    logging.debug(f"list_scopes : {list_scopes}")
    access_token = create_access_token(
        data={"sub": user.email, "scopes": list_scopes},
        expires_delta=access_token_expires,
    )
    return LoginResponse(access_token=access_token, token_type="bearer", user= user_base)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def check_token(
    #security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(db_connector.session)
):
    if token is None:
        raise unauthorizedError

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if email is None:
            raise unauthorizedError
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, email=email)
    except ExpiredSignatureError:
        logging.exception("expired token")
        raise expiredTokenError
    except (JWTError, ValidationError):
        logging.exception("jwt error")
        raise unauthorizedError

    return token_data



async def check_scopes(
        request : Request,
        security_scopes: SecurityScopes,
        token_data : Annotated[TokenData, Security(check_token)],
        #session: AsyncSession = Depends(db_connector.session),
):
    # router에서 선언한 scope
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        logging.debug(f'authenticate_value ={authenticate_value}')
    else:
        authenticate_value = "Bearer"
    # scope 확인
    isScope = False
    for scope in security_scopes.scopes:
        if scope in token_data.scopes:
            isScope = True
    if not isScope:
        raise noPermissionError

    # user = await select_by_email(session, email=token_data.email)
    # return UserResponse.model_validate(user)

async def logout(session: AsyncSession, token_data):
    logging.debug(f'logout :{token_data}')

async def verify(session: AsyncSession, email: str):
    #db에서 email로 조회 확인
    user = await select_by_email(session, email)
    if user is None:
        raise unauthorizedError
    return user

