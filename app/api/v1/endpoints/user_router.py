import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.core.web.response_base import Meta, Result, SodaflowResponseBase
from starlette import status

from app.core.sqlalchemy.database import db_connector
from app.schemas.userdto import UserResponse, UserCreate, UserUpdate, UserInitPassword
from app.services.user_service import read_users, create_user, update_user, delete_user, read_user, update_user_password

logger = logging.getLogger(__name__)

router = APIRouter()
@router.get("", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[List[UserResponse]])
async def request_users(db: AsyncSession = Depends(db_connector.session)):
    users = await read_users(db)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[List[UserResponse]](data=users, result=result, meta=meta)
    return response_data

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[UserResponse])
async def request_user(
        id: str,
        db: AsyncSession = Depends(db_connector.session)):
    logger.debug(f"id : {id}")
    user = await read_user(db, id)
    result = Result()
    meta = Meta(version='v1')
    user_rsp = UserResponse.model_validate(user.__dict__)
    response_data = SodaflowResponseBase[UserResponse](data=user_rsp, result=result, meta=meta)
    return response_data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SodaflowResponseBase[UserResponse])
async def request_create_user(
        user: UserCreate,
        session: AsyncSession = Depends(db_connector.session)
    ):
    logger.info(f"user : {user}")
    user = await create_user(session, user)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[UserResponse](data=user, result=result, meta=meta)
    return response_data

@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[UserResponse])
async def request_update_user(
        id: str,
        user: UserUpdate,
        session: AsyncSession = Depends(db_connector.session)):
    logger.info(f"user : {user}")
    updated_user = await update_user(session, id, user)
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[UserResponse](data=updated_user, result=Result(), meta=meta)
    return response_data

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase)
async def request_delete_user(
        id: str,
        session: AsyncSession = Depends(db_connector.session)):
    bool_result = await delete_user(session, id)
    data = dict(bool= bool_result)
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[dict](data=data, result=Result(), meta=meta)
    return response_data

# @router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase)
# async def request_delete_user(
#         id: int,
#         session: AsyncSession = Depends(db_connector.session)):
#     bool_result = await delete_user(session, id)
#     data = dict(bool= bool_result)
#     meta = Meta(version='v1')
#     response_data = SodaflowResponseBase[dict](data=data, result=Result(), meta=meta)
#     return response_data

@router.patch("/{id}/pass", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[UserResponse])
async def request_update_user_password(
        request: Request,
        id: str,
        user: UserInitPassword,
        session: AsyncSession = Depends(db_connector.session)
):
    updated_user = await update_user_password(session, request, id, user)
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[UserResponse](data=updated_user, result=Result(), meta=meta)
    return response_data
