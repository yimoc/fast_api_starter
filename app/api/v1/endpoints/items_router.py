import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.web.response_base import Meta, Result, SodaflowResponseBase
from starlette import status

from app.core.sqlalchemy.database import db_connector
from app.schemas.itemdto import ItemDto
from app.services.items_service import read_items, read_item, create_item, delete_item, update_item

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[List[ItemDto]])
async def request_items(db: AsyncSession = Depends(db_connector.get_async_session)):
    items = await read_items(db)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[List[ItemDto]](data=items, result=result, meta=meta)
    return response_data

@router.get("/{item_id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[ItemDto])
async def request_item(
        item_id: int,
        q: str = None,
        db: AsyncSession = Depends(db_connector.session)):
    logger.debug("item_id : %d", item_id)
    item = await read_item(db, item_id)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[ItemDto](data=item, result=result, meta=meta)
    return response_data


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SodaflowResponseBase[ItemDto])
async def request_create_item(
        item: ItemDto,
        session: AsyncSession = Depends(db_connector.session)
    ):
    logger.info(f"item : {item} : session : {session}")
    created_item = await create_item(session,item)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[ItemDto](data=created_item, result=result, meta=meta)
    return response_data

@router.put("/{item_id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[ItemDto])
async def request_update_item(
        item_id: int,
        item: ItemDto,
        session: AsyncSession = Depends(db_connector.session)):

    updated_item = await update_item(session, item_id, item)
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[ItemDto](data=updated_item, result=Result(), meta=meta)
    return response_data

@router.delete("/{item_id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase)
async def request_delete_item(
        item_id: int,
        session: AsyncSession = Depends(db_connector.session)):
    bool_result = await delete_item(session, item_id)
    data = dict(bool= bool_result)
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[dict](data=data, result=Result(), meta=meta)
    return response_data
'''
@router.get("/", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase)
def request_items_paginate(
        db: Session = Depends(get_db),
        page: Union[int, None] = None,
        page_size: Union[int, None] = None):
    page = read_items_page(db, page, page_size)
    result = Result()
    paginate = Paginate.parse_obj(page.__dict__)
    response_data = SodaflowResponseBase[list](data=page.items, result=result, meta=None, paginate=paginate)
'''


# @router.post("/put_queue", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase)
# async def request_put_queue(
#         session: AsyncSession = Depends(db_connector.session)):
#     parse_request = {
#         "document_set_id": "ABC",
#         "document_set_path": "123",
#         "org_pdf_path": "MDFSDFSDF",
#         "org_pdf_ids": "DFSDFSDF"
#     }
#     PARSING_QUEUE.put(parse_request)
#
#     data = dict(bool= True)
#     meta = Meta(version='v1')
#     response_data = SodaflowResponseBase[dict](data=data, result=Result(), meta=meta)
#     return response_data