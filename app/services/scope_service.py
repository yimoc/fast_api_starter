import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.transaction import SqlAlchemyTransaction, Transactional
from app.models.auth import Scope
from app.orm import scope_orm
from app.schemas.scopedto import ScopeResponse, ScopeCreate, ScopeUpdate

# create read update delete
logger = logging.getLogger(__name__)

async def read_scopes(session: AsyncSession) -> List[ScopeResponse]:
    result = await scope_orm.selects(session)
    return result


async def read_scope(session: AsyncSession, id: int) -> ScopeResponse:
    result = await scope_orm.select_by_id(session, id)
    return result

async def read_scope_by_permission(session: AsyncSession, permission: str) -> ScopeResponse:
    result = await scope_orm.select_by_permission(session, permission)
    return result


async def create_scope(session: AsyncSession, item: ScopeCreate):
    scope = Scope(**item.model_dump())
    logger.debug(f'insert scope = {scope}')
    scope = await scope_orm.insert(session, scope)
    return scope


@Transactional
async def update_scope(session: AsyncSession, id:int, item: ScopeUpdate):
    scope_record = Scope(**item.model_dump(), id=id)
    updated_count = await scope_orm.update(session, scope_record)
    return updated_count


@Transactional
async def delete_scope(session: AsyncSession, id: int) -> bool:
    deleted_count = await scope_orm.delete(session, id)
    return deleted_count




'''
from app.services.paginate import Page
def read_items_page(db: Session, page: int, page_size: int) -> Page:
    return orm.select_page(db, page, page_size)
'''
