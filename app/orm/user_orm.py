import logging
import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_404_NOT_FOUND

from app.core.exception.exceptions import SodaflowResponseError
from app.models.user import User
from app.orm import scope_orm
from app.orm.scope_orm import select_by_permission
from app.schemas.userdto import UserCreate, UserUpdate

logger = logging.getLogger(__name__)

async def selects(session: AsyncSession) -> list:
    result = await session.execute(select(User).options(selectinload(User.scopes)))
    return result.scalars().all()

async def select_by_id(session: AsyncSession, id: str) -> User:
    result = await session.execute(select(User).filter(User.id == id).options(selectinload(User.scopes)))
    return result.scalars().first()

# async def select_by_userid(session: AsyncSession, userid: str) -> User:
#     statement = select(User).where(
#         User.userid == userid
#     )
#     results = await session.execute(statement)
#     return results.unique().scalar_one_or_none()

async def select_by_email(session: AsyncSession, email: str) -> User:
    statement = select(User).where(
        User.email==email
    )
    results = await session.execute(statement)
    return results.unique().scalar_one_or_none()

async def select_by_name(session: AsyncSession, name: str) -> User:
    statement = select(User).where(
        User.name==name
    )
    results = await session.execute(statement)
    return results.unique().scalar_one_or_none()

async def insert(session: AsyncSession, user: UserCreate, hashed_password ):
    user_record = User(**user.model_dump(exclude=["password", "scopes"]), id=uuid.uuid4())
    user_record.hashed_password = hashed_password
    #scopes
    for scope in user.scopes:
        scope_result = await select_by_permission(session, scope.permission)
        logger.debug(f"scope_result ={scope_result}")
        user_record.scopes.append(scope_result)

    session.add(user_record)
    await session.commit()
    logger.debug(f"added ={user_record.id}")
    return user_record


async def update(session: AsyncSession, id, user: UserUpdate, hashed_password) -> User:
    selected_user = await select_by_id(session, id)

    if selected_user:
        # password 변경
        if user.password:
            selected_user.hashed_password = hashed_password

        # scope가 있는 경우 변경
        scopes = getattr(user,'scopes', None)
        if scopes and len(scopes) > 0:
            selected_user.scopes.clear()
            for scope in user.scopes:
                scope_result = await scope_orm.select_by_permission(session, scope.permission)
                selected_user.scopes.append(scope_result)
            logger.debug(f"scope_result ={selected_user.scopes}")

        # 기타 다른 데이터 변경
        for column in User.__table__.columns:
            if column != User.id and column != User.email and column != User.hashed_password \
                    and column != User.created_at and column != User.updated_at:
                set_value = getattr(user, column.name, None)
                if set_value:
                    setattr(selected_user, column.name, set_value)

        logger.debug(f"updated ={selected_user}")
        return selected_user
    else:
        raise SodaflowResponseError(
            status_code=HTTP_404_NOT_FOUND,
            code = "NotFound",
            message = f"Not found Id = {id}"
        )



async def delete_by_email(session: AsyncSession, email: str) -> bool:
    user = await session.get(User, email)
    if user:
        await session.delete(user)
        return True
    return False

async def delete(session: AsyncSession, id: str) -> bool:
    user = await session.get(User, id)
    if user:
        await session.delete(user)
        return True
    else:
        raise SodaflowResponseError(
            status_code=HTTP_404_NOT_FOUND,
            code = "NotFound",
            message = f"Not found Id = {id}"
        )




