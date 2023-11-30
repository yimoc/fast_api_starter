import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.transaction import SqlAlchemyTransaction, Transactional
from app.models.item import Item

from app.orm import items_orm as orm
from app.schemas.itemdto import ItemDto

# create read update delete

logger = logging.getLogger(__name__)

async def read_items(session: AsyncSession) -> list:
    result = await orm.selects(session)
    return result


async def read_item(session: AsyncSession, id: int) -> ItemDto:
    result = await orm.select_by_id(session, id)
    return result


#@Transactional
async def create_item(session: AsyncSession, item: ItemDto):
    db_item = Item(**item.model_dump())
    logger.info(f'insert item = {db_item}')
    db_item = await orm.insert(session, db_item)
    return db_item


@Transactional
async def update_item(session: AsyncSession, id: int, item: ItemDto):

    db_item = Item(**item.model_dump())
    updated_count = await orm.update(session, id, db_item)
    return updated_count


@Transactional
async def delete_item(session: AsyncSession, id: int) -> bool:
    deleted_count = await orm.delete(session, id)
    return deleted_count




'''
from app.services.paginate import Page
def read_items_page(db: Session, page: int, page_size: int) -> Page:
    return orm.select_page(db, page, page_size)
'''
