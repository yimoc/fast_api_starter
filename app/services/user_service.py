import base64
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from app.core.db.transaction import Transactional
from app.core.exception.exceptions import SodaflowResponseError
from app.models.user import User
from app.orm import user_orm
from app.schemas.userdto import UserResponse, UserCreate, UserUpdate, UserInitPassword
from app.services.password import get_password_hash

logger = logging.getLogger(__name__)

async def read_users(session: AsyncSession) -> list:
    result = await user_orm.selects(session)
    return result


async def read_user(session: AsyncSession, id: str) -> UserResponse:
    result = await user_orm.select_by_id(session, id)
    if not result:
        raise SodaflowResponseError(
            status_code=HTTP_404_NOT_FOUND,
            code="NotFound",
            message=f"Not found Id = {id}"
        )
    return result

async def read_user_by_email(session: AsyncSession, email: str) -> UserResponse:
    result = await user_orm.select_by_email(session, email)
    return result


# @Transactional :사용 시 Can't operate on closed transaction inside context manager.  Please complete the context manager before emitting further commands.
async def create_user(session: AsyncSession, user: UserCreate) -> UserResponse:
    #checking email 중복
    dupliated_email = await user_orm.select_by_email(session, user.email)
    if dupliated_email:
        raise SodaflowResponseError(
            status_code=HTTP_409_CONFLICT,
            code="DuplicatedEmail",
            message=f"Duplicated Email = {user.email}"
        )
    await check_duplicate_name(session, user.name)

    #hashing a password
    hashed_password = get_password_hash(user.password)
    logger.debug(f'passwrod = {user.password} ->  hashed_password = {hashed_password}')
    result = await user_orm.insert(session, user, hashed_password)
    return result

@Transactional
async def update_user(session: AsyncSession, id: str, user: UserUpdate):
    await check_duplicate_name(session, getattr(user,'name', None))

    hashed_password = None
    if user.password:
        hashed_password = get_password_hash(user.password)
        logger.debug(f'passwrod = {user.password} ->  hashed_password = {hashed_password}')
    updated_user = await user_orm.update(session, id, user, hashed_password)
    return updated_user


@Transactional
async def delete_user_by_email(session: AsyncSession, id: int) -> bool:
    deleted_bool = await user_orm.delete(session, id)
    return deleted_bool

@Transactional
async def delete_user(session: AsyncSession, id: str) -> bool:
    deleted_bool = await user_orm.delete(session, id)
    return deleted_bool

@Transactional
async def update_user_password( session: AsyncSession, request: Request, id: str, user: UserInitPassword):
    #client에서 hash했으면 진행
    encrypted = getattr(user, "hash", None)
    if encrypted:
        user.password = decryptRSA(request, encrypted)
        logger.debug(f'descrypted password = {user.password}')

    hashed_password = None
    if user.password:
        hashed_password = get_password_hash(user.password)
        logger.debug(f'passwrod = {user.password} ->  hashed_password = {hashed_password}')
    updated_user = await user_orm.update(session, id, user, hashed_password)
    return updated_user


async def check_duplicate_name(session: AsyncSession, name):
    if name:
        dupliated_name = await user_orm.select_by_name(session, name)
        if dupliated_name:
            raise SodaflowResponseError(
                status_code=HTTP_409_CONFLICT,
                code="DuplicatedName",
                message=f"Duplicated Name = {name}"
            )