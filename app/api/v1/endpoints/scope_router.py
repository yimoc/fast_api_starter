import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.web.response_base import Meta, Result, SodaflowResponseBase
from starlette import status

from app.core.sqlalchemy.database import db_connector
from app.schemas.scopedto import ScopeResponse, ScopeCreate, ScopeUpdate
from app.services.scope_service import read_scopes, read_scope, create_scope, update_scope, delete_scope

logger = logging.getLogger(__name__)

router = APIRouter()
@router.get("", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[List[ScopeResponse]])
async def request_scopes(db: AsyncSession = Depends(db_connector.session)):
    scopes = await read_scopes(db)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[List[ScopeResponse]](data=scopes, result=result, meta=meta)
    return response_data

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[ScopeResponse])
async def request_scope(
        id: int,
        db: AsyncSession = Depends(db_connector.session)):
    logger.debug(f"id : {id}")
    scope = await read_scope(db, id)
    result = Result()
    meta = Meta(version='v1')
    if scope is not None:
        user_rsp = ScopeResponse.model_validate(scope.__dict__)
    else:
        user_rsp = None
    response_data = SodaflowResponseBase[ScopeResponse](data=user_rsp, result=result, meta=meta)
    return response_data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SodaflowResponseBase[ScopeResponse])
async def request_create_scope(
        req_scope: ScopeCreate,
        session: AsyncSession = Depends(db_connector.session)
    ):
    logger.info(f"scope : {req_scope}")
    created_scope = await create_scope(session, req_scope)
    result = Result()
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[ScopeResponse](data=created_scope, result=result, meta=meta)
    return response_data

@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase[ScopeResponse])
async def request_update_scope(
        id: int,
        scope: ScopeUpdate,
        session: AsyncSession = Depends(db_connector.session)):
    logger.info(f"user : {scope}")
    updated_scope = await update_scope(session, id, scope)
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[ScopeResponse](data=updated_scope, result=Result(), meta=meta)
    return response_data

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=SodaflowResponseBase)
async def request_delete_scope(
        id: int,
        session: AsyncSession = Depends(db_connector.session)):
    bool_result = await delete_scope(session, id)
    data = dict(bool= bool_result)
    meta = Meta(version='v1')
    response_data = SodaflowResponseBase[dict](data=data, result=Result(), meta=meta)
    return response_data
