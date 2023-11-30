import logging

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import Scope

logger = logging.getLogger(__name__)

async def selects(session: AsyncSession) -> list:
    result = await session.execute(select(Scope))
    return result.scalars().all()

async def select_by_id(session: AsyncSession, id: int) -> Scope:
    results = await session.execute(select(Scope).filter(Scope.id == id))
    return results.unique().scalar_one_or_none()

async def select_by_permission(session: AsyncSession, permission: str) -> Scope:
    statement = select(Scope).where(
        Scope.permission == permission
    )
    results = await session.execute(statement)
    return results.unique().scalar_one_or_none()

async def insert(session: AsyncSession, scope: Scope):
    session.add(scope)
    await session.commit()
    return scope


async def update(session: AsyncSession, scope: Scope) -> Scope:
    selected_scope = await select_by_id(session, scope.id)
    if selected_scope:
        for column in scope.__table__.columns:
            setattr(selected_scope, column.name, getattr(scope, column.name))
    return selected_scope


async def delete(session: AsyncSession, id: int) -> bool:
    item = await session.get(Scope, id)
    if item:
        await session.delete(item)
        return True
    return False

    # id확인 필요
    # statement = delete(Scope).where(Scope.id == id)
    # results = await session.execute(statement)
    # logger.debug(results.__dict__)
    # return True




