import logging
from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from app.core.web.response_base import Meta, Result, SodaflowResponseBase

from fastapi import APIRouter,status

from app.core.sqlalchemy.database import db_connector
from app.models.user import User
from app.schemas.authdto import LoginResponse, Key, UserLogin
from app.schemas.userdto import UserResponse
from app.services.auth_service import login, check_token, TokenData, check_scopes, verify, logout

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[LoginResponse])
async def request_login(
    request: Request,
    user: UserLogin,
    session: AsyncSession = Depends(db_connector.session)
):
    result = Result()
    meta = Meta(version='v1')
    user = await login(request, session, user)
    response_data = SodaflowResponseBase[LoginResponse](data=user, result=result, meta=meta)
    return response_data

@router.post("/logout", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[None])
async def request_logout(
    request: Request,
    response: Response,
    token_data: Annotated[TokenData, Depends(check_token)],
    session: AsyncSession = Depends(db_connector.session)
):
    result = Result()
    meta = Meta(version='v1')
    user = await logout(session, token_data)
    response_data = SodaflowResponseBase[None](data=None, result=result, meta=meta)
    return response_data

#https://fastapi.tiangolo.com/advanced/advanced-dependencies/
@router.get("/verify", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[UserResponse])
async def request_verify(
        request: Request,
        token_data: Annotated[TokenData, Depends(check_token)],
        session: AsyncSession = Depends(db_connector.session)
):
    result = Result()
    meta = Meta(version='v1')
    user = await verify(session, token_data.email)
    response_data = SodaflowResponseBase[UserResponse](data=user, result=result, meta=meta)
    return response_data

# =========================================================================================================
# 하단은 테스트 용
# =========================================================================================================
@router.post("/loginForm", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def test_login_Form(
        request: Request,
        #user: UserLogin,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(db_connector.session),
):
    """
    fastapi의 /docs(swagger) test를 위한 url
        /login과 동일하게 유지해야한다. Formdata로 수신하여 진행한다.
        username을 email로 사용해야한다.
        oauth2_scheme 의 url을 수정해야한다.
    :param request:
    :param form_data:
    :param session:
    :return:
    """
    result = Result()
    meta = Meta(version='v1')
    user = User()
    user.email = form_data.username
    user.password = form_data.password
    loginresponse = await login(request, session, user)
    return loginresponse

@router.get("/sesion/test", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[None])
async def test_session_key(request: Request):
    """
    session의 값을 확인하기 위한 테스트
    :param request:
    :return:
    """
    result = Result()
    meta = Meta(version='v1')
    logger.debug(f'session PK = {request.session.get("_private_key", None)[:50]}')
    response_data = SodaflowResponseBase[Key](data=None, result=result, meta=meta)
    return response_data

@router.get("/permission_user", status_code=status.HTTP_200_OK,  response_model=SodaflowResponseBase[None])
async def test_permission_user(
    current_user: Annotated[UserResponse, Security(check_scopes, scopes=["user", "admin"])]
):
    """
    user permission test용
    :param current_user:
    :return:
    """
    result = Result()
    meta = Meta(version='v1')
    data = current_user
    response_data = SodaflowResponseBase[None](data=None, result=result, meta=meta)
    return response_data

@router.get("/permission_admin", status_code=status.HTTP_200_OK,  response_model=SodaflowResponseBase[None])
async def test_permission_admin(
    current_user: Annotated[UserResponse, Security(check_scopes, scopes=["admin"])]
):
    """
    admin 퍼미션 확인용
    :param current_user:
    :return:
    """
    result = Result()
    meta = Meta(version='v1')
    data = current_user
    response_data = SodaflowResponseBase[None](data=None, result=result, meta=meta)
    return response_data
