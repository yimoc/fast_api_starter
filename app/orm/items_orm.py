import logging

from sqlalchemy import select
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item

# select, insert, update, delete
# from app.services.paginate import Page, paginate

logger = logging.getLogger(__name__)

async def selects(session: AsyncSession) -> list:
    result = await session.execute(select(Item))
    return result.scalars().all()


async def selects_offset(session: AsyncSession, offset: int, limit: int) -> list:
    result = await session.execute(select(Item).offset(offset).limit(limit))
    return result.scalars().all()


async def select_by_id(session: AsyncSession, id: int) -> Item:
    result = await session.execute(select(Item).filter(Item.id == id))
    return result.scalars().first()


async def insert(session: AsyncSession, item: Item):
    # logger.info(f"test : {item}")
    item.id = None  #id를 지정할 경우 해당 id의 값으로 load되어 리턴된다.(autoincrement인경우)
    session.add(item)
    await session.commit()
    print(f"added ={item}")
    return item


async def update(session: AsyncSession, id: int, des_item: Item) -> Item:
    item = await session.get(Item, id)
    if item:
        for column in Item.__table__.columns:
            setattr(item, column.name, getattr(des_item, column.name))
    return item


async def delete(session: AsyncSession, id: int) -> bool:
    item = await session.get(Item, id)
    if item:
        await session.delete(item)
        return True
    return False


# def select_filters(session: AsyncSession, filter) -> list:
#     query = session.query(models.Item)
#     for attr, value in filter.items():
#         print(attr)
#         query = query.filter(getattr(models.Item, attr) == value)
#     return query.all()
''' 작업중
# https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
def select_order_by(session: Session, orderby: str) -> list:
    query = session.query(models.Item)
    # sort = asc(sort_column) if sort_dir == "desc" else desc(sort_column)
    
    #    order_list = orderby.split(',')
    #for order_key in order_list:
    #    query.order_by(order_key)
     
    # query.order_by(desc('id'))
    query.order_by(models.Item.id.desc())
    return session.query()

def select_page(session: Session, page, page_size) -> Page:
    query = session.query(models.Item)
    return paginate(query, page, page_size)
'''
